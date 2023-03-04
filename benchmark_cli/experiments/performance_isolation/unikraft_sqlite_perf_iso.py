import time
import logging as log

from helpers.unikraft_benchmark_helpers import run_unikraft_sqlite_benchmark_instance
from helpers.unikraft_helpers import run_unikraft, clean_all_vms

EXPERIMENT_NAME = "uk_sqlite_perf_iso_r"

ATTACKER_NAME = "read_attack"
SAME_CORE = 1


def run_two_unikrafts(core_1, core_2, file_name, run_index, attack):
    taskset_text = ""
    if core_2 != -1:
        taskset_text=f"taskset {core_2}"

    run_unikraft(
        ip_address=None,
        instance_cnt=None,
        name=attack,
        taskset_text=taskset_text,
    )
    time.sleep(25)

    run_unikraft_sqlite_benchmark_instance(
        f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-{file_name}.out", core_1
    )


def run_unikraft_sqlite_perf_iso_experiment(run_index, benchmark_times, instances_per_benchmark):
    run_unikraft_sqlite_benchmark_instance(
        f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-single.out", SAME_CORE
    )

    time.sleep(10)
    log.info("Single SQLite benchmark completed")

    log.info("Running benchmark on same core, same thread")

    run_two_unikrafts(SAME_CORE, SAME_CORE, "same-thread", run_index, ATTACKER_NAME)
    log.info("Benchmark completed")