from experiments.docker_nginx_experiment import run_docker_nginx_experiment
from experiments.docker_nginx_parallel_experiment import run_docker_nginx_parallel_experiment
from experiments.unikraft_nginx_experiment import run_unikraft_nginx_experiment
from experiments.unikraft_nginx_parallel_experiment import run_unikraft_nginx_parallel_experiment
from experiments.docker_redis_parallel_experiment import run_docker_redis_parallel_experiment
from experiments.unikraft_redis_parallel_experiment import run_unikraft_redis_parallel_experiment
from experiments.docker_redis_experiment import run_docker_redis_experiment
from experiments.unikraft_redis_experiment import run_unikraft_redis_experiment
from experiments.unikraft_boot_experiment import run_unikraft_boot_experiment
from experiments.docker_boot_experiment import run_docker_boot_experiment
from experiments.unikraft_cpu_parallel_experiment import run_unikraft_cpu_parallel_experiment
from experiments.docker_cpu_parallel_experiment import run_docker_cpu_parallel_experiment
from helpers.docker_helpers import clean_all_containers
from helpers.unikraft_helpers import clean_all_vms
import logging as log
import time

import click

EXPERIMENT_NAMES = [
    # Nginx experiments
    "uk_ng_s",
    "d_ng_s",
    "d_ng_p",
    "uk_ng_p",
    # Redis experiments
    "d_re_p",
    "d_re_s",
    "uk_re_p",
    "uk_re_s",
    # Boot experiments
    "uk_boot",
    "d_boot",
    # CPU performance experiments
    "uk_cpu_p",
    "d_cpu_p",
]

log.basicConfig(
    level=log.INFO, filename="/dev/stdout",
    format="%(levelname)s: %(message)s"
)


@click.command(help="CLI tool for spawning lightweight virtualization systems")
@click.option(
    '-r', '--runs',
    type=int,
    help='Number of instances to spawn as part of the experiment',
    required=True,
)
@click.option(
    '-n', '--name',
    type=str,
    help='Name of image to use',
    required=True,
)
@click.option(
    '-bt', '--benchmark_times',
    type=int,
    help="Number of times benchmarked",
    required=False,
    default=5,
)
@click.option(
    '-ib', '--instances_per_benchmark',
    type=int,
    help="Number of instances between benchmarks",
    required=False,
    default=10,
)
def experiment_runner(runs, name, benchmark_times, instances_per_benchmark):
    if name not in EXPERIMENT_NAMES:
        log.error(f"Experiment named {name} not found")
        exit()

    for ind in range(1, runs+1):
        log.info(f"Starting run: {ind}")
        run_experiment(name, ind, benchmark_times, instances_per_benchmark)
        log.info("Benchmark finished. Starting cleaning process")

        start_time = time.time()
        clean_experiment(name)
        end_time = time.time()

        log.info(f"Cleaning took: {end_time - start_time:.3f}")


def run_experiment(name, ind, benchmark_times, instances_per_benchmark):
    if name == "d_ng_s":
        run_docker_nginx_experiment(ind, benchmark_times, instances_per_benchmark)
    elif name == "d_ng_p":
        run_docker_nginx_parallel_experiment(ind)
    elif name == "uk_ng_s":
        run_unikraft_nginx_experiment(ind, benchmark_times, instances_per_benchmark)
    elif name == "uk_ng_p":
        run_unikraft_nginx_parallel_experiment(ind)
    elif name == "d_re_p":
        run_docker_redis_parallel_experiment(ind)
    elif name == "uk_re_p":
        run_unikraft_redis_parallel_experiment(ind)
    elif name == "d_re_s":
        run_docker_redis_experiment(ind, benchmark_times, instances_per_benchmark)
    elif name == "uk_re_s":
        run_unikraft_redis_experiment(ind, benchmark_times, instances_per_benchmark)
    elif name == "uk_boot":
        run_unikraft_boot_experiment(ind, benchmark_times, instances_per_benchmark)
    elif name == "d_boot":
        run_docker_boot_experiment(ind, benchmark_times, instances_per_benchmark)
    elif name == "uk_cpu_p":
        run_unikraft_cpu_parallel_experiment(ind, benchmark_times, instances_per_benchmark)
    elif name == "d_cpu_p":
        run_docker_cpu_parallel_experiment(ind, benchmark_times, instances_per_benchmark)


def clean_experiment(name):
    if name in ["d_ng_s", "d_ng_p", "d_re_p", "d_re_s", "d_boot", "d_cpu_p"]:
        clean_all_containers()
    elif name in ["uk_ng_s", "uk_ng_p", "uk_re_p", "uk_re_s", "uk_boot", "uk_cpu_p"]:
        clean_all_vms()
        time.sleep(30)
    else:
        log.error("Error: benchmark data not cleaned after run")


if __name__ == "__main__":
    experiment_runner()
