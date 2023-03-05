import time
import logging as log

from helpers.docker_helpers import create_container_taskset, \
    clean_all_containers, create_container_taskset_static
from helpers.wrk_helpers import run_wrk_benchmark

EXPERIMENT_NAME = "d_nginx_perf_iso"
SAME_CORE = 1
BUSY_CONTAINER_NAME = "busy-container"


def run_two_containers(taskset_1, taskset_2, file_name, run_index):
    create_container_taskset(port_in=80, port_out=8080, image_name="nginx-benchmark", taskset_text=taskset_1)
    create_container_taskset_static(image_name=BUSY_CONTAINER_NAME, taskset_text=taskset_2)

    time.sleep(25)
    run_wrk_benchmark(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-{file_name}.out", "localhost:8080")


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

    clean_all_containers()
    time.sleep(10)

    log.info("Running benchmark on same core, same thread")

    run_two_containers(f"taskset {SAME_CORE}", f"taskset {SAME_CORE}", "same-thread", run_index)
    log.info("Benchmark completed")