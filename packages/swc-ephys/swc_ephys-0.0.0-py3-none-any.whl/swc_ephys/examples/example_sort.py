from pathlib import Path

from swc_ephys.pipeline.sort import run_sorting

base_path = Path(
    r"/ceph/neuroinformatics/neuroinformatics/scratch/jziminski/ephys/test_data/steve_multi_run/1119617/time-mid"
)
sub_name = "1119617"
run_name = "1119617_LSE1_shank12_posttest1_pretest1"

preprocessed_data_path = (
    base_path / "derivatives" / sub_name / f"{run_name}" / "preprocessed"
)


if __name__ == "__main__":
    # sorting uses multiprocessing so must be in __main__
    run_sorting(
        preprocessed_data_path,
        sorter="kilosort2_5",
        sorter_options={"kilosort2_5": {"car": False}},
        overwrite_existing_sorter_output=False,
        slurm_batch=False,
    )
