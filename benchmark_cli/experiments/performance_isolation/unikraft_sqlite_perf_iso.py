import time
import logging as log

from helpers.unikraft_benchmark_helpers import run_unikraft_sqlite_benchmark_instance
from helpers.unikraft_helpers import run_unikraft, clean_all_vms

EXPERIMENT_NAME = "uk_sqlite_perf_iso_fork"

ATTACKER_NAME = "fork_bomb"
SAME_CORE = 1

CORE_27 = "0x8000000"
CORE_79 = "0x80000000000000000000"  # Same Core as hyperthread 27
CORE_85 = "0x2000000000000000000000"  # Same CPU as hyperthread 27
CORE_15 = "0x8000"  # Different CPU node


def run_two_unikrafts(core_1, core_2, file_name, run_index, attack, instances_per_benchmark):
    taskset_text = ""
    if core_2 != -1:
        taskset_text=f"taskset {core_2}"

    run_unikraft(
        ip_address=None,
        instance_cnt=None,
        name=attack,
        taskset_text=taskset_text,
    )
    time.sleep(5)

    for i in range(instances_per_benchmark):
        run_unikraft_sqlite_benchmark_instance(
            f"benchmark-data/{EXPERIMENT_NAME}/{run_index * instances_per_benchmark + i}-{file_name}.out", core_1
        )
        time.sleep(1)

    clean_all_vms()
    time.sleep(5)


def run_unikraft_sqlite_perf_iso_experiment(run_index, benchmark_times, instances_per_benchmark):
    for i in range(instances_per_benchmark):
        run_unikraft_sqlite_benchmark_instance(
            f"benchmark-data/{EXPERIMENT_NAME}/{run_index*instances_per_benchmark + i}-single.out", CORE_27
        )
        time.sleep(1)

    log.info("Single run completed")

    run_two_unikrafts(
        core_1=CORE_27,
        core_2=CORE_27,
        run_index=run_index,
        file_name="same-thread",
        instances_per_benchmark=instances_per_benchmark
    )

    log.info("Same thread run completed")

    run_two_unikrafts(
        core_1=CORE_27,
        core_2=CORE_79,
        run_index=run_index,
        file_name="same-core",
        instances_per_benchmark=instances_per_benchmark
    )

    log.info("Same core run completed")

    run_two_unikrafts(
        core_1=CORE_27,
        core_2=CORE_85,
        run_index=run_index,
        file_name="same-cpu",
        instances_per_benchmark=instances_per_benchmark
    )

    log.info("Same CPU run completed")

    run_two_unikrafts(
        core_1=CORE_27,
        core_2=CORE_15,
        run_index=run_index,
        file_name="same-machine",
        instances_per_benchmark=instances_per_benchmark
    )

    log.info("Same machine run completed")

    log.info("Benchmark completed")