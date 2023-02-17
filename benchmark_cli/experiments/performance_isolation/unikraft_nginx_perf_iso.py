import time
import logging as log

from helpers.unikraft_benchmark_helpers import run_unikraft_cpu_benchmark_instance
from helpers.unikraft_helpers import setup_network, run_unikraft, clean_all_vms
from helpers.wrk_helpers import run_wrk_benchmark

EXPERIMENT_NAME = "uk_nginx_perf_iso"

CORE1_ID = 1
CORE2_ID = 2


def run_two_unikrafts(taskset_1, taskset_2, file_name, run_index):
    run_unikraft(
        ip_address="172.16.0.2",
        instance_cnt=1,
        name="nginx",
        taskset_text=taskset_1,
    )

    run_unikraft(
        ip_address=None,
        instance_cnt=None,
        name="busy",
        taskset_text=taskset_2,
    )
    time.sleep(25)
    run_wrk_benchmark(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-{file_name}.out", "172.16.0.2")


def run_unikraft_nginx_perf_iso_experiment(run_index, benchmark_times, instances_per_benchmark):
    ips_required = 1
    setup_network(ips_required)
    log.info("Network setup ready")

    run_unikraft(
        ip_address="172.16.0.2",
        instance_cnt=1,
        name="nginx",
        taskset_text="",
    )

    time.sleep(25)
    log.info("Main VM started. Starting first wrk benchmark")

    run_wrk_benchmark(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-single.out", "172.16.0.2")
    log.info("Single run completed")

    clean_all_vms()
    time.sleep(10)

    log.info("Running benchmark with automatic scheduling")

    run_two_unikrafts("" "", "auto", run_index)
    clean_all_vms()
    time.sleep(10)


    log.info("Running benchmark on same core, separate threads")

    run_two_unikrafts("taskset 1", "taskset 2", "diff-thread", run_index)
    clean_all_vms()
    time.sleep(10)

    log.info("Running benchmark on same core, same thread")

    run_two_unikrafts("taskset 1", "taskset 1", "same-thread", run_index)
    log.info("Benchmark completed")