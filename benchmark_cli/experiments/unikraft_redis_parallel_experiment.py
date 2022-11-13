import time
import logging as log

from helpers.unikraft_helpers import run_unikraft, setup_network
from helpers.redis_benchmark_helpers import run_redis_benchmark

EXPERIMENT_NAME = "uk_re_p"
INSTANCES = 5


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

    for unikernel in range(INSTANCES):
        run_unikraft(
            ip_address=ips[active_vms],
            instance_cnt=active_vms + 1,
            name="redis",
        )
        active_vms += 1

    time.sleep(50)
    log.info(f"Started {INSTANCES} unikernels. Performing benchmark now")

    for i in range(INSTANCES):
        run_redis_benchmark(ips[i], 6379, f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-{i}.out")

    time.sleep(15)
    log.info("Benchmark finished. Continuing!")
