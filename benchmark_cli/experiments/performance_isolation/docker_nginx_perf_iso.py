import time
import logging as log

from helpers.docker_helpers import create_container_taskset
from helpers.wrk_helpers import run_wrk_benchmark, network_stress_attacker

EXPERIMENT_NAME = "d_nginx_perf_iso"
SAME_CORE = 1
BUSY_CONTAINER_NAME = "busy-container"


def run_docker_nginx_perf_iso_experiment(run_index, benchmark_times, instances_per_benchmark):
    create_container_taskset(
        port_in=80,
        port_out=8080,
        image_name="nginx-benchmark",
        taskset_text=f"taskset {SAME_CORE}"
    )

    time.sleep(10)
    log.info("Main container started. Starting first wrk benchmark")

    run_wrk_benchmark(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-single.out", "localhost:8080")
    log.info("Single run completed")

    log.info("Running benchmark on same core, same thread")

    create_container_taskset(
        port_in=8123,
        port_out=7070,
        image_name="server-attacker",
        taskset_text=f"taskset {SAME_CORE}"
    )
    network_stress_attacker(ip_address="127.0.0.1:7070", sleep_time=30)
    run_wrk_benchmark(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-single.out", "localhost:8080")
    log.info("Benchmark completed")
