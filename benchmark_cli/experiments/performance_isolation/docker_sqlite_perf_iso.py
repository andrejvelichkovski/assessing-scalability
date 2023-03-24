import time
import logging as log

from helpers.docker_benchmark_helpers import run_docker_sqlite_benchmark
from helpers.docker_helpers import create_container_taskset_static, clean_all_containers
from helpers.unikraft_benchmark_helpers import run_unikraft_sqlite_benchmark_instance
from helpers.unikraft_helpers import run_unikraft, clean_all_vms

EXPERIMENT_NAME = "d_sqlite_perf_iso"

MAIN_CORE = 27
SAME_CORE = 79
SAME_CPU = 85
SAME_MACHINE = 15

ATTACKER_NAME = "read_attack"


def run_two_containers(core_1, core_2, file_name, run_index, attack, instances_per_benchmark):
    print(EXPERIMENT_NAME)
    taskset_text = ""
    if core_2 != -1:
        taskset_text = f"taskset {core_2}"

    create_container_taskset_static(
        image_name=attack,
        taskset_text=taskset_text,
        tmpfs="--mount type=tmpfs,destination=/app",
    )

    time.sleep(10)

    for i in range(instances_per_benchmark):
        run_docker_sqlite_benchmark(
            file_name=f"benchmark-data/{EXPERIMENT_NAME}/{(run_index - 1) * instances_per_benchmark + i}-{file_name}.out",
            core=core_1,
            wait_to_complete=True
        )
        time.sleep(1)

    clean_all_containers()
    time.sleep(1)


def run_docker_sqlite_perf_iso_experiment(run_index, benchmark_times, instances_per_benchmark):
    for i in range(instances_per_benchmark):
        run_docker_sqlite_benchmark(
            file_name=f"benchmark-data/{EXPERIMENT_NAME}/{(run_index - 1) * instances_per_benchmark + i}-single.out",
            core=MAIN_CORE,
            wait_to_complete=True,
        )
        time.sleep(1)

    log.info("Single SQLite benchmark completed")

    run_two_containers(MAIN_CORE, SAME_CORE, "same-thread", run_index, ATTACKER_NAME, instances_per_benchmark)
    log.info("Same core benchmark completed")

    run_two_containers(MAIN_CORE, SAME_CPU, "same-cpu", run_index, ATTACKER_NAME, instances_per_benchmark)
    log.info("Same CPU benchmark completed")

    run_two_containers(MAIN_CORE, SAME_MACHINE, "same-machine", run_index, ATTACKER_NAME, instances_per_benchmark)
    log.info("Same machine benchmark completed")
