import time
import logging as log

from helpers.unikraft_helpers import run_unikraft, setup_network
from helpers.redis_benchmark_helpers import run_redis_benchmark, get_redis_benchmark_process

EXPERIMENT_NAME = "uk_re_p_tmp"
INSTANCES = 128
RUN_BENCHMARK_PLACES = [1, 2, 4, 8, 16, 32, 64, 128]
WAIT_BETWEEN_INSTANCES = 2


def run_unikraft_redis_parallel_experiment(run_index):
    INSTANCES_PER_IP = 200
    ips_required = (INSTANCES + INSTANCES_PER_IP - 1) // INSTANCES_PER_IP

    setup_network(ips_required)
    log.info("Network setup ready")

    ips = []
    active_vms = 0
    for i in range(ips_required):
        for j in range(INSTANCES_PER_IP):
            if active_vms == INSTANCES:
                break

            current_ip = f"172.{16 + i}.0.{2 + j}"
            ips.append(current_ip)
            active_vms += 1

    active_vms = 0

    for unikernel in range(1, INSTANCES+1):
        run_unikraft(
            ip_address=ips[active_vms],
            instance_cnt=active_vms + 1,
            name="redis",
        )
        active_vms += 1
        time.sleep(WAIT_BETWEEN_INSTANCES)

        if unikernel in RUN_BENCHMARK_PLACES:
            log.info(f"Started {unikernel} unikernels in total. Performing benchmarks now")
            benchmark_processes = []
            for i in range(unikernel):
                benchmark_processes.append(
                    get_redis_benchmark_process(
                        ips[i],
                        6379,
                        f"benchmark-data/{EXPERIMENT_NAME}/{unikernel}-data-{i}.out"
                    )
                )

            for p in benchmark_processes:
                p.wait()

    time.sleep(5)
    log.info("Benchmark finished. Continuing!")
