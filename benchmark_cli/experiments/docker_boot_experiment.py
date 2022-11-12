import time

from helpers.docker_helpers import create_container_static, start_container
from helpers.docker_benchmark_helpers import run_docker_boot_benchmark
import logging as log

EXPERIMENT_NAME = "d_boot"
INSTANCES = 50

log.basicConfig(
    level=log.INFO, filename="/dev/stdout",
    format="%(levelname)s: %(message)s"
)


def run_docker_boot_experiment(run_index):

    log.info("Main container started. Starting first boot benchmark")

    run_docker_boot_benchmark(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-single.out")
    for i in range(5):
        for cont in range(INSTANCES):
            container = create_container_static("sleep-container")
            start_container(container)

        time.sleep(10)
        log.info(f"Started {INSTANCES} additional containers. Performing new benchmark now")

        run_docker_boot_benchmark(
            f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-{(i+1)*INSTANCES}.out"
        )
        log.info("Benchmark finished. Continuing!")
