import time
import logging as log

from helpers.docker_benchmark_helpers import run_docker_cpu_benchmark

EXPERIMENT_NAME = "d_cpu_p"


def run_docker_cpu_parallel_experiment(run_index, benchmark_times, instances_per_benchmark):
    run_docker_cpu_benchmark(
        file_name=f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-single.out",
        core=-1,
        wait_to_complete=True,
    )

    log.info("Single run completed")

    cores = [1, 4]
    for index, core in enumerate(cores):
        run_docker_cpu_benchmark(
            file_name=f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-{index}.out",
            core=core,
            wait_to_complete=False,
        )
    time.sleep(15)

    log.info("Core specified benchmark completed")

    for index in range(2):
        run_docker_cpu_benchmark(
            file_name=f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-os-{index}.out",
            core=-1,
            wait_to_complete=False,
        )
    time.sleep(15)

    log.info("Benchmark completed")