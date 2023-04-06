import time
import logging as log

from helpers.system_usage_helpers import measure_system_usage
from helpers.unikraft_helpers import run_unikraft
from helpers.unikraft_benchmark_helpers import run_unikraft_boot_benchmark_instance

EXPERIMENT_NAME = "uk_mem"


def run_unikraft_mem_experiment(run_index, benchmark_times, instances_per_benchmark):
    # run_unikraft_boot_benchmark_instance(f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-single.out")
    run_unikraft(
        ip_address=None,
        instance_cnt=None,
        name="sleeping",
    )
    active_vms = 1
    measure_system_usage(
        f"benchmark-data/{EXPERIMENT_NAME}",
        run_index,
        "single",
    )
    log.info("Finished first boot benchmark")

    for i in range(benchmark_times):
        for unikernel in range(instances_per_benchmark):
            if active_vms == (i+1) * instances_per_benchmark:
                continue

            run_unikraft(
                ip_address=None,
                instance_cnt=None,
                name="sleeping",
            )

        time.sleep(instances_per_benchmark)
        log.info(f"Started {instances_per_benchmark} additional containers. Performing new benchmark now")

        # run_unikraft_boot_benchmark_instance(
        #     f"benchmark-data/{EXPERIMENT_NAME}/{run_index}-data-{(i+1)*instances_per_benchmark}.out"
        # )
        # Possibly the QEMU might detach the previous VM slightly earlier
        # to avoid race-condition we wait a few seconds before monitoring
        # the system usage
        time.sleep(5)
        measure_system_usage(
            f"benchmark-data/{EXPERIMENT_NAME}",
            run_index,
            (i+1)*instances_per_benchmark,
        )
        log.info("Benchmark finished. Continuing!")
