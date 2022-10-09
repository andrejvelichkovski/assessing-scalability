"""
This CLI tool is used for benchmarking Docker performance on scale

For given image name and container count (c) it launches c images

Usage:

python3 docker_micro_benchmark --containers X --image_name Y

Optional flags:
* --no_clean_flag: specifies to skip the closing of images after 
all of them are launched. WARNING: This leaves c images hunging 
around on the OS after this operation is performed
"""

import click

from docker import APIClient

import logging as log
import statistics
import time

log.basicConfig(
    level=log.INFO, filename="/dev/stdout",
    format="%(levelname)s: %(message)s"
)

docker_cli = APIClient(base_url="unix:///run/docker.sock")

def clean_containers(active_containers):
    log.info("Starting process of cleaning created containers")

    for id in active_containers:
        docker_cli.kill(id)

    log.info("Process of cleaning created containers completed")


@click.command()
@click.option(
    '-c', '--containers',
    type=int,
    help='Number of containers created as part of the experiment',
    required=True,
)
@click.option(
    '-i', '--image',
    type=str,
    help='Name of Docker image to use',
    required=True,
)
@click.option(
    '--no_clean_flag',
    is_flag=True,
    help='Flag to specify whether to skip cleaning containers after experiment',
)
def docker_micro_benchmark(containers, image, no_clean_flag):
    if no_clean_flag:
        log.warning("You have specified the no clean flag!")
        log.warning(f"This experiment will create {containers} conainers without cleaning them!")

    if containers % 10 != 0:
        log.error("Invalid Input: Please enter containers as number divisible by 10")
        exit()

    create_array = []
    start_array = []

    active_containers = []


    for i in range(containers):

        # Print benchmark progress
        if i % (containers // 10) == 0:
            log.info(f"Benchmark progress: { (i // (containers // 10) + 1) * 10 }%")

        host_config = docker_cli.create_host_config(
            port_bindings={80: 8080+i}
        )

        # Creating container
        start = time.time()
        container = docker_cli.create_container(image=image, host_config=host_config)
        end = time.time()

        active_containers.append(container.get("Id"))

        create_array.append(end - start)

        # Starting container
        start = time.time()
        docker_cli.start(container.get("Id"))
        end = time.time()

        start_array.append(end - start)

    log.info("Benchmark outputs:")

    log.info("create stats")
    for i in range(containers // 10):
        print(i, statistics.mean(create_array[i*10:(i+1)*10]))

    log.info("start stats")
    for i in range(containers // 10):
        print(i, statistics.mean(start_array[i*10:(i+1)*10]))

    if not no_clean_flag:
        clean_containers(active_containers)

if __name__ == '__main__':
    docker_micro_benchmark()