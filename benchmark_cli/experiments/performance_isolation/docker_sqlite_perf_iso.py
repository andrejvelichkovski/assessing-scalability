import time
import logging as log

from helpers.docker_benchmark_helpers import run_docker_sqlite_benchmark
from helpers.docker_helpers import create_container_taskset_static, clean_all_containers
from helpers.unikraft_benchmark_helpers import run_unikraft_sqlite_benchmark_instance
from helpers.unikraft_helpers import run_unikraft, clean_all_vms

EXPERIMENT_NAME = "d_sqlite_perf_iso"

CORE1_ID = 1
CORE2_ID = 2

ATTACKER_NAME = "read_attack"


def run_two_containers(core_1, core_2, file_name, run_index):
    print(EXPERIMENT_NAME)
    taskset_text = ""
    if core_2 != -1:
        taskset_text=f"taskset {core_2}"

    create_container_taskset_static(image_name="write-attacker", taskset_text=taskset_text)

    time.sleep(20)

    run_docker_sqlite_benchmark(
        file_name=f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-{file_name}.out",
        core=core_1,
        wait_to_complete=True
    )


def run_docker_sqlite_perf_iso_experiment(run_index, benchmark_times, instances_per_benchmark):
    run_docker_sqlite_benchmark(
        file_name=f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-single.out",
        core=-1,
        wait_to_complete=True
    )
    time.sleep(10)
    log.info("Single SQLite benchmark completed")

    log.info("Running benchmark with automatic scheduling")

    run_two_containers(-1, -1, "auto", run_index)
    clean_all_containers()
    time.sleep(10)

    log.info("Running benchmark on same core, separate threads")

    run_two_containers(1, 2, "diff-thread", run_index)
    clean_all_containers()
    time.sleep(10)

    log.info("Running benchmark on same core, same thread")

    run_two_containers(1, 1, "same-thread", run_index)
    log.info("Benchmark completed")