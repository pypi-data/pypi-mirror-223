from __future__ import annotations

import copy
import gc
import shutil
import time
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Literal, Tuple, Union

if TYPE_CHECKING:
    from ..data_classes.preprocessing import PreprocessingData
    from ..data_classes.sorting import SortingData

from ..configs.configs import get_configs
from ..pipeline.load_data import load_data_for_sorting
from ..utils import slurm, utils
from ..utils.custom_types import HandleExisting
from .load_data import load_spikeglx_data
from .postprocess import run_postprocess
from .preprocess import preprocess
from .sort import run_sorting


def run_full_pipeline(
    base_path: Union[Path, str],
    sub_name: str,
    run_names: Union[List[str], str],
    config_name: str = "default",
    sorter: str = "kilosort2_5",
    existing_preprocessed_data: HandleExisting = "load_if_exists",
    existing_sorting_output: HandleExisting = "load_if_exists",
    overwrite_postprocessing: bool = False,
    postprocessing_to_run: Union[Literal["all"], Dict] = "all",
    delete_intermediate_files: Tuple[
        Literal["preprocessed", "recording.dat", "temp_wh.dat", "waveforms"]
    ] = (
        "recording.dat",
    ),  # TODO: use new spikeinterface settings for kilosort.
    verbose: bool = True,
    slurm_batch: bool = False,
) -> None:
    """
    Run preprocessing, sorting and post-processing on SpikeGLX data.
    see README.md for detailed information on use. If waveforms and
    postprocessing exist for the subjects / runs, it will be
    overwritten.

    This function must be run in main as uses multiprocessing e.g.
    if __name__ == "__main__":
        run_full_pipeline(args...)

    Parameters
    ----------
    base_path : Union[Path, str]
        Path to the rawdata folder containing subjects folders.

    sub_name : str
        Subject to preprocess. The subject top level dir should reside in
        base_path/rawdata/ .

    run_names : Union[List[str], str],
        The SpikeGLX run name (i.e. not including the gate index). This can
        also be a list of run names. Preprocessing will still occur per-run.
        Runs are concatenated in the order passed prior to sorting.

    config_name : str
        The name of the configuration to use. Note this must be the name
        of a .yaml file (not including the extension) stored in
        swc_ephys/configs.

    sorter : str
        name of the sorter to use e.g. "kilosort2_5".

    existing_preprocessed_data : Literal["overwrite", "load_if_exists", "fail_if_exists"]
        Determines how existing preprocessed data (e.g. from a prior pipeline run)
        is treated.
            "overwrite" : will overwrite any existing preprocessed data output. This will
                          delete the 'preprocessed' folder. Therefore, never save
                          derivative work there.
            "load_if_exists" : will search for existing data and load if it exists.
                               Otherwise, will use the preprocessing from the
                               current run.
            "fail_if_exists" : If existing preprocessed data is found, an error
                               will be raised.

    existing_sorting_output : bool
        Determines how existing sorted data is treated. The same behaviour
        as `existing_preprocessed_data` but for sorting output. If overwrite,
        the 'sorting' folder will be deleted. Therefore, never save
        derivative work there.

    overwrite_postprocessing : bool
        If `False`, an error will be raised if postprocessing output already
        exists. Otherwise, 'postprocessing' folder will be overwritten. Note,
        that the entire 'postprocessing' folder (including all contents) will be
        deleted. Therefore, never save derivative work there.

    postprocessing_to_run : Union[Literal["all"], Dict]
        Specify the postprocessing to run. By default, "all" will run
        all available postprocessing. Otherwise, provide a dict of
        including postprocessing to run e.g. {"quality_metrics: True"}.

    delete_intermediate_files : Tuple[Union["preprocessing", "recording.dat", "temp_wh.dat", "waveforms"]]  # TODO: check types
        Specify intermediate files or folders to delete. This option is useful for
        reducing the size of output data by deleting unneeded files.

        preprocessing  - the 'preprocesed' folder holding the data that has been
                         preprocessed by SpikeInterface
        recording.dat - SpikeInterfaces copies the preprocessed data to folder
                        prior to sorting, where it resides in the 'sorter_output'
                        folder. Often, this can be deleted after sorting.
        temp_wh.dat - Kilosort output file that holds the data preprocessed by
                      Kilosort (e.g. drift correction). By default, this is used
                      for visualisation in Phy.
        waveforms - The waveform outputs that SpikeInterface generates to calculate
                    quality metrics. Often, these can be deleted once final quality
                    metrics are computed.

    verbose : bool
        If True, messages will be printed to console updating on the
        progress of preprocessing / sorting.

    slurm_batch : bool
        If True, the pipeline will be run in a SLURM job. Set False
        if running on an interactive job, or locally.
    """
    if slurm_batch:
        local_args = copy.deepcopy(locals())
        slurm.run_full_pipeline_slurm(**local_args)
        return
    assert slurm_batch is False, "SLURM run has slurm_batch set True"

    pp_steps, sorter_options, waveform_options = get_configs(config_name)

    preprocess_data = load_spikeglx_data(base_path, sub_name, run_names)

    preprocess_data = preprocess(preprocess_data, pp_steps, verbose)

    save_preprocessed_data_if_required(preprocess_data, existing_preprocessed_data)

    sorting_data = run_or_get_sorting(
        preprocess_data, existing_sorting_output, sorter, sorter_options, verbose
    )

    sorting_data.set_sorter_output_paths(sorter)
    delete_postprocessing_output_if_it_exists(sorting_data, overwrite_postprocessing)

    run_postprocess(
        sorting_data,
        sorter,
        existing_waveform_data="fail_if_exists",
        postprocessing_to_run=postprocessing_to_run,
        verbose=verbose,
        waveform_options=waveform_options,
    )

    handle_delete_intermediate_files(sorting_data, delete_intermediate_files)


def handle_delete_intermediate_files(sorting_data, delete_intermediate_files):
    """ """
    if "preprocessed" in delete_intermediate_files:
        # remove the existing link to the preprocessed data binary.
        # wait time of 5 s is arbitrary.
        # TODO: this feels very hacky. Can unlink the memory map from the segment?
        # Ask SI.
        del sorting_data["0-preprocessed"]
        gc.collect()
        time.sleep(5)

        if sorting_data.preprocessed_data_path.is_dir():
            shutil.rmtree(sorting_data.preprocessed_data_path)

    if "recording.dat" in delete_intermediate_files:
        if (
            recording_file := sorting_data.sorter_run_output_path / "recording.dat"
        ).is_file():
            recording_file.unlink()

    if "temp_wh.dat" in delete_intermediate_files:
        if (
            recording_file := sorting_data.sorter_run_output_path / "temp_wh.dat"
        ).is_file():
            recording_file.unlink()

    if "waveforms" in delete_intermediate_files:
        if (
            waveforms_path := sorting_data.postprocessing_output_path / "waveforms"
        ).is_dir():
            shutil.rmtree(waveforms_path)


def delete_postprocessing_output_if_it_exists(
    sorting_data: SortingData, overwrite_postprocessing: bool
):
    """
    If previous postprocessing output exists, it must be deleted before
    the new postprocessing is run. As a safety measure, `overwrite_postprocessing`
    must be set to `True` to perform the deletion.
    """
    if sorting_data.postprocessing_output_path.is_dir():
        if overwrite_postprocessing:
            utils.message_user(
                f"Deleting existing postprocessing "
                f"output at {sorting_data.postprocessing_output_path}"
            )
            shutil.rmtree(sorting_data.postprocessing_output_path)
        else:
            raise RuntimeError(
                f"Postprocessing output already exists at "
                f"{sorting_data.postprocessing_output_path} "
                f"but `overwrite_postprocessing` is `False`. Setting "
                f"`overwrite_postprocessing` will delete the postprocessing "
                f"folder and all it's contents."
            )


def run_or_get_sorting(
    preprocess_data: PreprocessingData,
    existing_sorting_output: HandleExisting,
    sorter: str,
    sorter_options: Dict,
    verbose: bool,
) -> SortingData:
    """
    Handle existing sorting output. If previous output exists, load, error or
    overwrite according to `existing_sorting_output`. See `run_full_pipeline()` for details.
    """
    # TODO: "sorting" to configs. In general handle this function better
    # it should not be on preprocess_data. It could be a classmethod on
    # SortingData but this may be even messier.
    sorting_path = preprocess_data.get_expected_sorter_path(sorter) / "sorting"

    if sorting_path.is_dir() and existing_sorting_output == "load_if_exists":
        utils.message_user(f"Loaded pre-existing sorting output from {sorting_path}")

        sorting_data = load_data_for_sorting(
            preprocess_data.preprocessed_data_path,
        )

    elif sorting_path.is_dir() and existing_sorting_output == "fail_if_exists":
        raise RuntimeError(
            f"Sorting output already exists at {sorting_path} and"
            f"`existing_sorting_output` is set to 'fail_if_exists'."
        )

    else:
        utils.message_user("Running sorting...")

        overwrite_existing_sorter_output = True

        sorting_data = run_sorting(
            preprocess_data.preprocessed_data_path,
            sorter,
            sorter_options,
            overwrite_existing_sorter_output,
            verbose,
        )

    return sorting_data


def save_preprocessed_data_if_required(
    preprocess_data: PreprocessingData,
    existing_preprocessed_data: Literal[
        "overwrite", "load_if_exists", "fail_if_exists"
    ],
) -> None:
    """
    Handle the loading of existing preprocessed data.
    See `run_full_pipeline()` for details.
    """
    preprocess_path = preprocess_data.preprocessed_data_path

    if existing_preprocessed_data == "overwrite":
        if preprocess_path.is_dir():
            utils.message_user(f"Removing existing file at {preprocess_path}\n")

        utils.message_user(f"Saving preprocessed data to {preprocess_path}")

        preprocess_data.save_all_preprocessed_data(overwrite=True)

    elif existing_preprocessed_data == "load_if_exists":
        if preprocess_path.is_dir():
            utils.message_user(
                f"\nSkipping preprocessing, using file at "
                f"{preprocess_path} for sorting.\n"
            )
        else:
            utils.message_user(
                f"No data found at {preprocess_path}, saving" f"preprocessed data."
            )
            preprocess_data.save_all_preprocessed_data(overwrite=False)

    elif existing_preprocessed_data == "fail_if_exists":
        if preprocess_path.is_dir():
            raise FileExistsError(
                f"Preprocessed binary already exists at "
                f"{preprocess_path}. "
                f"To overwrite, set 'existing_preprocessed_data' to 'overwrite'"
            )
        preprocess_data.save_all_preprocessed_data(overwrite=False)

    else:
        raise ValueError(
            "`existing_preproessed_data` argument not recognised."
            "Must be: 'load_if_exists', 'fail_if_exists' or 'overwrite'."
        )
