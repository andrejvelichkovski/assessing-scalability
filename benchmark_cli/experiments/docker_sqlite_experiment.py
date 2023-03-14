import time

from helpers.docker_benchmark_helpers import run_docker_sqlite_benchmark
from helpers.docker_helpers import start_container, create_container_static

import logging as log

from helpers.system_usage_helpers import measure_system_usage

EXPERIMENT_NAME = "d_sqlite_s"

log.basicConfig(
    level=log.INFO, filename="/dev/stdout",
    format="%(levelname)s: %(message)s"
)


def run_docker_sqlite_experiment(run_index, benchmark_times, instances_per_benchmark):
    run_docker_sqlite_benchmark(
        file_name=f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-single.out",
        core=-1,
        wait_to_complete=True
    )
    measure_system_usage(
        f"benchmark-data/{EXPERIMENT_NAME}",
        run_index,
        "single",
    )
    time.sleep(10)

    log.info("Benchmark finished. Continuing!")

    for i in range(benchmark_times):
        for cont in range(instances_per_benchmark):
            container = create_container_static("sleep-container")
            start_container(container)

        time.sleep(instances_per_benchmark)
        log.info(f"Started {instances_per_benchmark} additional containers. Performing new benchmark now")

        run_docker_sqlite_benchmark(
            file_name=f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-{(i+1)*instances_per_benchmark}.out",
            core=-1,
            wait_to_complete=True
        )
        measure_system_usage(
            f"benchmark-data/{EXPERIMENT_NAME}",
            run_index,
            (i+1)*instances_per_benchmark,
        )
        time.sleep(10)
        log.info("Benchmark finished. Continuing!")