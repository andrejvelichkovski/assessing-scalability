import time
import logging as log

from helpers.unikraft_helpers import run_unikraft, setup_network
from helpers.wrk_helpers import run_wrk_benchmark

EXPERIMENT_NAME = "uk_ng_s"
INSTANCES = 10


def run_unikraft_nginx_experiment(run_index):
    INSTANCES_PER_IP = 200
    ips_required = (5 * INSTANCES + 1 + INSTANCES_PER_IP - 1) // INSTANCES_PER_IP

    setup_network(ips_required)
    log.info("Network setup ready")

    ips = []
    active_vms = 0
    for i in range(ips_required):
        for j in range(INSTANCES_PER_IP):
            if active_vms == 5 * INSTANCES + 1:
                break

            current_ip = f"172.{16 + i}.0.{2 + j}"
            ips.append(current_ip)
            active_vms += 1

    active_vms = 0
    run_unikraft(
        ip_address=ips[active_vms],
        instance_cnt=active_vms+1,
        name="nginx",
    )
    active_vms += 1
    time.sleep(25)
    log.info("Main VM started. Starting first wrk benchmark")

    run_wrk_benchmark(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-single.out", ips[0])
    time.sleep(10)
    log.info("Benchmark finished. Continuing!")

    for i in range(5):
        for unikernel in range(INSTANCES):
            run_unikraft(
                ip_address=ips[active_vms],
                instance_cnt=active_vms+1,
                name="nginx",
            )
            active_vms += 1

        time.sleep(35)
        log.info(f"Started {INSTANCES} additional containers. Performing new benchmark now")

        run_wrk_benchmark(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-{(i+1)*INSTANCES}.out", ips[0])
        time.sleep(10)
        log.info("Benchmark finished. Continuing!")
