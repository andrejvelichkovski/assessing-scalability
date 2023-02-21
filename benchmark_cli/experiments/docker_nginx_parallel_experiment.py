import time

from helpers.docker_helpers import create_container, start_container
from helpers.wrk_helpers import get_wrk_benchmark_process

import logging as log

EXPERIMENT_NAME = "d_ng_p_tmp"
INSTANCES = 128
RUN_BENCHMARK_PLACES = [1, 2, 4, 8, 16, 32, 64, 128]
WAIT_BETWEEN_INSTANCES = 2


log.basicConfig(
    level=log.INFO, filename="/dev/stdout",
    format="%(levelname)s: %(message)s"
)


def run_docker_nginx_parallel_experiment(run_index):
    log.info("Starting containers")

    active_port = 8080
    for container_id in range(1, INSTANCES+1):
        container = create_container(80, active_port, "nginx-benchmark")
        start_container(container)
        active_port += 1
        time.sleep(WAIT_BETWEEN_INSTANCES)

        if container_id in RUN_BENCHMARK_PLACES:
            log.info(f"Started {container_id} containers in total. Performing benchmarks now")
            benchmark_processes = []
            for i in range(container_id):
                benchmark_processes.append(
                    get_wrk_benchmark_process(
                        f"benchmark-data/{EXPERIMENT_NAME}/{container_id}-data-{i}.out",
                        f"localhost:{8080 + i}",
                    )
                )

            for p in benchmark_processes:
                p.wait()
        time.sleep(5)

    log.info("Benchmark finished. Continuing!")
