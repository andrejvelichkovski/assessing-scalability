import time
import logging as log

from helpers.unikraft_helpers import setup_network, run_unikraft, clean_all_vms
from helpers.wrk_helpers import run_wrk_benchmark, network_stress_attacker

EXPERIMENT_NAME = "uk_nginx_perf_iso"
SAME_CORE = 1
BUSY_VM_NAME = "busy"


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
        name=BUSY_VM_NAME,
        taskset_text=taskset_2,
    )
    time.sleep(25)
    run_wrk_benchmark(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-{file_name}.out", "172.16.0.2")


def run_unikraft_nginx_perf_iso_experiment(run_index, benchmark_times, instances_per_benchmark):
    ips_required = 2
    setup_network(ips_required)
    log.info("Network setup ready")

    run_unikraft(
        ip_address="172.16.0.2",
        instance_cnt=1,
        name="nginx",
        taskset_text=f"taskset {SAME_CORE}",
    )

    time.sleep(25)
    log.info("Main VM started. Starting first wrk benchmark")

    run_wrk_benchmark(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-single.out", "172.16.0.2")
    log.info("Single run completed")

    run_unikraft(
        ip_address="172.16.0.3",
        instance_cnt=2,
        name="httpreply_attack",
        taskset_text=f"taskset {SAME_CORE}",
    )

    time.sleep(10)

    network_stress_attacker(ip_address="172.16.0.3:8123", sleep_time=25)
    run_wrk_benchmark(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-single.out", "172.16.0.2")

    log.info("Benchmark completed")