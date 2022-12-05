import time

from helpers.docker_helpers import create_container_static, start_container
from helpers.docker_benchmark_helpers import run_docker_boot_benchmark
from helpers.system_usage_helpers import measure_system_usage
import logging as log

EXPERIMENT_NAME = "d_boot"

log.basicConfig(
    level=log.INFO, filename="/dev/stdout",
    format="%(levelname)s: %(message)s"
)


def run_docker_boot_experiment(run_index, benchmark_times, instances_per_benchmark):
    log.info("Main container started. Starting first boot benchmark")
    run_docker_boot_benchmark(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-single.out")
    measure_system_usage(
        f"benchmark-data/{EXPERIMENT_NAME}",
        run_index,
        "single",
    )
    for i in range(benchmark_times):
        for cont in range(instances_per_benchmark):
            container = create_container_static("sleep-container")
            start_container(container)

        time.sleep(10)
        log.info(f"Started {instances_per_benchmark} additional containers. Performing new benchmark now")

        run_docker_boot_benchmark(
            f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-{(i+1)*instances_per_benchmark}.out"
        )
        measure_system_usage(
            f"benchmark-data/{EXPERIMENT_NAME}",
            run_index,
            (i+1)*instances_per_benchmark,
        )
        log.info("Benchmark finished. Continuing!")
