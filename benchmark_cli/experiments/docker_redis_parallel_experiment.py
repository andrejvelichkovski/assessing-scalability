import subprocess

import time

from helpers.docker_helpers import create_container, start_container
from helpers.redis_benchmark_helpers import run_redis_benchmark
import logging as log

EXPERIMENT_NAME = "d_re_p"
INSTANCES = 5

log.basicConfig(
    level=log.INFO, filename="/dev/stdout",
    format="%(levelname)s: %(message)s"
)


def run_docker_redis_parallel_experiment(run_index):
    log.info("Starting containers")

    active_port = 8080
    for cont in range(INSTANCES):
        container = create_container(6379, active_port, "redis-benchmark")
        start_container(container)
        active_port += 1

    time.sleep(10)
    log.info(f"Started {INSTANCES} containers. Performing new benchmark now")

    port = 8080
    for i in range(INSTANCES):
        run_redis_benchmark("localhost", port, f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-{i}.out")
        port += 1
    time.sleep(10)
    log.info("Benchmark finished. Continuing!")
