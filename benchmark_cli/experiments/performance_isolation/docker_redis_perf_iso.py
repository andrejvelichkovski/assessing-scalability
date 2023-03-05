import time
import logging as log

from helpers.docker_helpers import create_container_taskset, \
    clean_all_containers, create_container_taskset_static
from helpers.redis_benchmark_helpers import run_redis_benchmark
EXPERIMENT_NAME = "d_redis_perf_iso"
SAME_CORE = 1
BUSY_CONTAINER_NAME = "busy-container"


def run_two_containers(taskset_1, taskset_2, file_name, run_index):
    create_container_taskset(port_in=6379, port_out=8080, image_name="redis-benchmark", taskset_text=taskset_1)
    create_container_taskset_static(image_name=BUSY_CONTAINER_NAME, taskset_text=taskset_2)

    time.sleep(25)
    run_redis_benchmark("localhost", "8080", f"./benchmark-data/{EXPERIMENT_NAME}/{run_index}-{file_name}.out")


def run_docker_redis_perf_iso_experiment(run_index, benchmark_times, instances_per_benchmark):
    create_container_taskset(
        port_in=6379,
        port_out=8080,
        image_name="redis-benchmark",
        taskset_text=f"taskset {SAME_CORE}"
    )
    time.sleep(10)

    log.info("Main container started. Starting first wrk benchmark")

    run_redis_benchmark("localhost", "8080", f"./benchmark-data/{EXPERIMENT_NAME}/{run_index}-single.out")
    log.info("Single run completed")

    clean_all_containers()
    time.sleep(10)

    log.info("Running benchmark on same core, same thread")

    run_two_containers(f"taskset {SAME_CORE}", f"taskset {SAME_CORE}", "same-thread", run_index)
    log.info("Benchmark completed")