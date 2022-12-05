import time

from helpers.docker_helpers import create_container, start_container
from helpers.redis_benchmark_helpers import run_redis_benchmark

import logging as log

from helpers.system_usage_helpers import measure_system_usage

EXPERIMENT_NAME = "d_re_s"

log.basicConfig(
    level=log.INFO, filename="/dev/stdout",
    format="%(levelname)s: %(message)s"
)


def run_docker_redis_experiment(run_index, benchmark_times, instances_per_benchmark):
    active_port = 8080

    container = create_container(6379, active_port, "redis-benchmark")
    start_container(container)

    active_port += 1

    time.sleep(2)
    log.info("Main container started. Starting first wrk benchmark")

    run_redis_benchmark(
        "localhost",
        8080,
        f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-single.out"
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
            container = create_container(6379, active_port, "redis-benchmark")
            start_container(container)
            active_port += 1

        time.sleep(2)
        log.info(f"Started {instances_per_benchmark} additional containers. Performing new benchmark now")

        run_redis_benchmark(
            "localhost",
            8080,
            f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-{(i+1)*instances_per_benchmark}.out"
        )
        measure_system_usage(
            f"benchmark-data/{EXPERIMENT_NAME}",
            run_index,
            (i+1)*instances_per_benchmark,
        )
        time.sleep(10)
        log.info("Benchmark finished. Continuing!")
