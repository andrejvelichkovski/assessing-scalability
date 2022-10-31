import subprocess

import time

from helpers.docker_helpers import create_container, start_container
import logging as log

EXPERIMENT_NAME = "d_ng_p"
INSTANCES = 5

log.basicConfig(
    level=log.INFO, filename="/dev/stdout",
    format="%(levelname)s: %(message)s"
)


def run_wrk_benchmark(file_data, ip_address, port):
    subprocess.Popen(
        f"wrk -d 1m -c 30 -t 14 http://{ip_address}:{port} > {file_data}",
        shell=True
    )


def run_docker_nginx_parallel_experiment(run_index):
    log.info("Starting containers")

    active_port = 8080
    for cont in range(INSTANCES):
        container = create_container(active_port, "nginx-benchmark")
        start_container(container)
        active_port += 1

    time.sleep(10)
    log.info(f"Started {INSTANCES} containers. Performing new benchmark now")

    port = 8080
    for i in range(INSTANCES):
        run_wrk_benchmark(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-{i}.out", "localhost", port)
        port += 1
    time.sleep(70)
    log.info("Benchmark finished. Continuing!")
