import os
import subprocess
import time
import logging as log

from helpers.unikraft_helpers import run_unikraft
from helpers.unikraft_benchmark_helpers import run_unikraft_boot_benchmark_instance

EXPERIMENT_NAME = "uk_boot"
INSTANCES = 5


def run_unikraft_boot_experiment(run_index):
    run_unikraft_boot_benchmark_instance(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-single.out")
    log.info("Finished first boot benchmark")

    for i in range(5):
        for unikernel in range(INSTANCES):
            run_unikraft(
                ip_address=None,
                instance_cnt=None,
                name="sleeping",
            )

        time.sleep(5)
        log.info(f"Started {INSTANCES} additional containers. Performing new benchmark now")

        run_unikraft_boot_benchmark_instance(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-{(i+1)*INSTANCES}.out")
        time.sleep(5)
        log.info("Benchmark finished. Continuing!")
