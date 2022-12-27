import time
import logging as log

from helpers.unikraft_benchmark_helpers import run_unikraft_cpu_benchmark_instance

EXPERIMENT_NAME = "uk_cpu_p"


def run_unikraft_cpu_parallel_experiment(run_index, benchmark_times, instances_per_benchmark):
    run_unikraft_cpu_benchmark_instance(
        file_name=f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-single.out",
        core=-1,
        wait_to_complete=True,
    )

    log.info("Single run completed")

    cores = [1, 4]
    for index, core in enumerate(cores):
        run_unikraft_cpu_benchmark_instance(
            file_name=f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-{index}.out",
            core=core,
            wait_to_complete=False,
        )
    time.sleep(15)

    log.info("Core specified benchmark completed")

    for index in range(2):
        run_unikraft_cpu_benchmark_instance(
            file_name=f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-os-{index}.out",
            core=-1,
            wait_to_complete=False,
        )
    time.sleep(15)

    log.info("Benchmark completed")