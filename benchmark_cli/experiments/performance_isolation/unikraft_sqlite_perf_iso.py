import time
import logging as log

from helpers.unikraft_benchmark_helpers import run_unikraft_sqlite_benchmark_instance
from helpers.unikraft_helpers import run_unikraft, clean_all_vms

EXPERIMENT_NAME = "uk_sqlite_perf_iso"

CORE1_ID = 1
CORE2_ID = 2

ATTACKER_NAME = "read_attack"


def run_two_unikrafts(core_1, core_2, file_name, run_index):
    print(EXPERIMENT_NAME)
    taskset_text = ""
    if core_2 != -1:
        taskset_text=f"taskset {core_2}"

    run_unikraft(
        ip_address=None,
        instance_cnt=None,
        name=ATTACKER_NAME,
        taskset_text=taskset_text,
    )
    time.sleep(25)

    run_unikraft_sqlite_benchmark_instance(
        f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-{file_name}.out", core_1
    )


def run_unikraft_sqlite_perf_iso_experiment(run_index, benchmark_times, instances_per_benchmark):
    run_unikraft_sqlite_benchmark_instance(
        f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-single.out"
    )

    time.sleep(10)
    log.info("Single SQLite benchmark completed")

    log.info("Running benchmark with automatic scheduling")

    run_two_unikrafts(-1, -1, "auto", run_index)
    clean_all_vms()
    time.sleep(10)

    log.info("Running benchmark on same core, separate threads")

    run_two_unikrafts(1, 2, "diff-thread", run_index)
    clean_all_vms()
    time.sleep(10)

    log.info("Running benchmark on same core, same thread")

    run_two_unikrafts(1, 1, "same-thread", run_index)
    log.info("Benchmark completed")