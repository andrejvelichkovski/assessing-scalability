import time
import logging as log

from helpers.docker_helpers import create_container_taskset, \
    clean_all_containers, create_container_taskset_static
from helpers.redis_benchmark_helpers import run_redis_benchmark
EXPERIMENT_NAME = "d_redis_perf_iso"
BUSY_CONTAINER_NAME = "busy-container"

MAIN_CORE = 27
SAME_CORE = 79
SAME_CPU = 85
SAME_MACHINE = 15

def run_two_containers(main_taskset, attack_taskset, file_name, run_index, instances_per_benchmark):
    create_container_taskset(port_in=6379, port_out=8080, image_name="redis-benchmark", taskset_text=main_taskset)
    create_container_taskset_static(image_name=BUSY_CONTAINER_NAME, taskset_text=attack_taskset)
    time.sleep(5)

    for i in range(instances_per_benchmark):
        log.info(f"./benchmark-data/{EXPERIMENT_NAME}/{(run_index - 1) * instances_per_benchmark+ i}-{file_name}.out")
        run_redis_benchmark(
            "localhost",
            "8080",
            f"./benchmark-data/{EXPERIMENT_NAME}/{(run_index - 1) * instances_per_benchmark + i}-{file_name}.out"
        )
        time.sleep(1)


def run_docker_redis_perf_iso_experiment(run_index, benchmark_times, instances_per_benchmark):
    create_container_taskset(
        port_in=6379,
        port_out=8080,
        image_name="redis-benchmark",
        taskset_text=f"taskset {MAIN_CORE}"
    )
    time.sleep(10)

    log.info("Main container started. Starting first wrk benchmark")

    for i in range(instances_per_benchmark):
        log.info(f"./benchmark-data/{EXPERIMENT_NAME}/{(run_index - 1) * instances_per_benchmark + i}-single.out")
        run_redis_benchmark(
            "localhost",
            "8080",
            f"./benchmark-data/{EXPERIMENT_NAME}/{(run_index - 1) * instances_per_benchmark + i}-single.out"
        )
        time.sleep(1)

    log.info("Single run completed")

    clean_all_containers()
    time.sleep(5)

    log.info("Running benchmark on same core, same thread")

    run_two_containers(
        f"taskset {MAIN_CORE}", f"taskset {MAIN_CORE}", "same-thread", run_index, instances_per_benchmark
    )
    clean_all_containers()
    time.sleep(5)

    run_two_containers(
        f"taskset {MAIN_CORE}", f"taskset {SAME_CORE}", "same-core", run_index, instances_per_benchmark
    )
    log.info("Benchmark completed")