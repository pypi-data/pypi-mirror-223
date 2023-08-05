from pathlib import Path

from swc_ephys.pipeline.full_pipeline import run_full_pipeline

base_path = Path(
    "/ceph/neuroinformatics/neuroinformatics/scratch/jziminski/ephys/test_data/steve_multi_run/1119617/time-short"
)
#    r"C:\data\ephys\test_data\steve_multi_run\1119617\time-short"
sub_name = "1119617"
run_names = [
    "1119617_LSE1_shank12",
    "1119617_posttest1_shank12",
    "1119617_pretest1_shank12",
]

config_name = "default"
sorter = "mountainsort5"  #  "kilosort2_5"  # "spykingcircus" # mountainsort5

if __name__ == "__main__":
    run_full_pipeline(
        base_path,
        sub_name,
        run_names,
        config_name,
        sorter,
        existing_preprocessed_data="load_if_exists",
        existing_sorting_output="overwrite",
        overwrite_postprocessing=True,
        slurm_batch=False,
    )
