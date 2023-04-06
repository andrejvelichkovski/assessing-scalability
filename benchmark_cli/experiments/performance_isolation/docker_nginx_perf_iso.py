import time
import logging as log

from helpers.docker_helpers import create_container_taskset, create_container_taskset_static, clean_all_containers
from helpers.wrk_helpers import run_wrk_benchmark, network_stress_attacker

EXPERIMENT_NAME = "d_nginx_perf_iso"
SAME_CORE = 1
BUSY_CONTAINER_NAME = "busy-container"

MAIN_CORE = 27
SAME_CORE = 79
SAME_CPU = 85
SAME_MACHINE = 15


def run_two_containers(main_core, attack_core, file_name, run_index, instances_per_benchmark):
    create_container_taskset(
        port_in=80,
        port_out=8080,
        image_name="nginx-benchmark",
        taskset_text=f"taskset {main_core}"
    )

    create_container_taskset_static(
        image_name=BUSY_CONTAINER_NAME,
        taskset_text=f"taskset {attack_core}",
    )

    time.sleep(5)

    for i in range(instances_per_benchmark):
        log.info(f"benchmark-data/{EXPERIMENT_NAME}/{(run_index-1)*instances_per_benchmark + i}-{file_name}.out")
        run_wrk_benchmark(
            f"benchmark-data/{EXPERIMENT_NAME}/{(run_index-1)*instances_per_benchmark + i}-{file_name}.out",
            "localhost:8080",
        )
        time.sleep(1)

def run_docker_nginx_perf_iso_experiment(run_index, benchmark_times, instances_per_benchmark):
    create_container_taskset(
        port_in=80,
        port_out=8080,
        image_name="nginx-benchmark",
        taskset_text=f"taskset {MAIN_CORE}"
    )
    time.sleep(5)
    log.info("Main container started. Starting first wrk benchmark")

    for i in range(instances_per_benchmark):
        log.info(f"benchmark-data/{EXPERIMENT_NAME}/{(run_index-1)*instances_per_benchmark + i}-single.out")
        run_wrk_benchmark(
            f"benchmark-data/{EXPERIMENT_NAME}/{(run_index-1)*instances_per_benchmark + i}-single.out",
            "localhost:8080",
        )
        time.sleep(1)

    log.info("Single run completed")

    log.info("Running benchmark on same core, same thread")

    run_two_containers(MAIN_CORE, MAIN_CORE, "same-thread", run_index, instances_per_benchmark)

    clean_all_containers()
    log.info("same thread completed")

    run_two_containers(MAIN_CORE, SAME_CORE, "same-thread", run_index, instances_per_benchmark)

    log.info("same core completed")

    clean_all_containers()

    log.info("Benchmark completed")
