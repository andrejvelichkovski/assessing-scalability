import time
import logging as log

from helpers.unikraft_helpers import setup_network, run_unikraft, clean_all_vms
from helpers.wrk_helpers import run_wrk_benchmark, network_stress_attacker

EXPERIMENT_NAME = "uk_nginx_perf_iso"
SAME_CORE = 1
BUSY_VM_NAME = "busy"

CORE_27 = "0x8000000"
CORE_79 = "0x80000000000000000000"  # Same Core as hyperthread 27
CORE_85 = "0x2000000000000000000000"  # Same CPU as hyperthread 27
CORE_15 = "0x8000"  # Different CPU node


def run_two_unikrafts(taskset_1, taskset_2, file_name, run_index, instances_per_benchmark):
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
    time.sleep(5)

    for i in range(instances_per_benchmark):
        log.info(f"benchmark-data/{EXPERIMENT_NAME}/{(run_index-1)*instances_per_benchmark + i}-{file_name}.out")
        run_wrk_benchmark(
            f"benchmark-data/{EXPERIMENT_NAME}/{(run_index-1)*instances_per_benchmark + i}-{file_name}.out",
            "172.16.0.2"
        )
        time.sleep(1)


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

    for i in range(instances_per_benchmark):
        log.info(f"benchmark-data/{EXPERIMENT_NAME}/{(run_index - 1) * instances_per_benchmark + i}-single.out")
        run_wrk_benchmark(
            f"benchmark-data/{EXPERIMENT_NAME}/{(run_index - 1) * instances_per_benchmark + i}-single.out",
            "172.16.0.2"
        )
        time.sleep(1)

    log.info("Single run completed")
    clean_all_vms()
    time.sleep(5)

    run_two_unikrafts(f"taskset {CORE_27}", f"taskset {CORE_27}", "same-thread", run_index, instances_per_benchmark)
    clean_all_vms()
    time.sleep(5)

    log.info("same thread finished")

    run_two_unikrafts(f"taskset {CORE_27}", f"taskset {CORE_79}", "same-core", run_index, instances_per_benchmark)
    clean_all_vms()
    time.sleep(5)

    log.info("Benchmark completed")
