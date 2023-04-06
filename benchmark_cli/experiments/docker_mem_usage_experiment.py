import time

from helpers.docker_helpers import create_container_static, start_container
from helpers.docker_benchmark_helpers import run_docker_boot_benchmark
from helpers.system_usage_helpers import measure_system_usage
import logging as log

EXPERIMENT_NAME = "d_mem"

log.basicConfig(
    level=log.INFO, filename="/dev/stdout",
    format="%(levelname)s: %(message)s"
)


def run_docker_mem_experiment(run_index, benchmark_times, instances_per_benchmark):
    container = create_container_static("sleep-container")
    start_container(container)

    active_containers = 1

    measure_system_usage(
        f"benchmark-data/{EXPERIMENT_NAME}",
        run_index,
        "single",
    )

    for i in range(benchmark_times):
        for cont in range(instances_per_benchmark):
            if active_containers == (i+1) * instances_per_benchmark:
                continue

            container = create_container_static("sleep-container")
            start_container(container)
            active_containers += 1

        time.sleep(instances_per_benchmark)
        log.info(f"Started {instances_per_benchmark} additional containers. Performing new benchmark now")

        measure_system_usage(
            f"benchmark-data/{EXPERIMENT_NAME}",
            run_index,
            (i+1)*instances_per_benchmark,
        )
        log.info("Benchmark finished. Continuing!")
