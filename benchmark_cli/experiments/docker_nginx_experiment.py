import time

from helpers.docker_helpers import create_container, start_container
from helpers.wrk_helpers import run_wrk_benchmark
import logging as log

EXPERIMENT_NAME = "d_ng_s"
INSTANCES = 10

log.basicConfig(
    level=log.INFO, filename="/dev/stdout",
    format="%(levelname)s: %(message)s"
)


def run_docker_nginx_experiment(run_index):
    active_port = 8080

    container = create_container(80, active_port, "nginx-benchmark")
    start_container(container)

    active_port += 1

    time.sleep(2)
    log.info("Main container started. Starting first wrk benchmark")

    run_wrk_benchmark(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-single.out", "localhost:8080")
    time.sleep(100)
    log.info("Benchmark finished. Continuing!")

    for i in range(5):
        for cont in range(INSTANCES):
            container = create_container(80, active_port, "nginx-benchmark")
            start_container(container)
            active_port += 1

        time.sleep(2)
        log.info(f"Started {INSTANCES} additional containers. Performing new benchmark now")

        run_wrk_benchmark(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-{(i+1)*INSTANCES}.out", "localhost:8080")
        time.sleep(100)
        log.info("Benchmark finished. Continuing!")
