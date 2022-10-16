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

def docker_spawner(instances, name, clean_flag):
    if not clean_flag:
        log.warning(f"This experiment will create {instances} conainers without cleaning them!")

    if instances % 10 != 0:
        log.error("Invalid Input: Please enter containers as number divisible by 10")
        exit()

    # Arrays for keeping benchmark results
    create_array = []
    start_array = []

    active_containers = []
    for i in range(1, instances + 1):

        # Print benchmark progress
        if i % (instances // 10) == 0:
            log.info(f"Benchmark progress: { (i // (instances // 10)) * 10 }%")

        host_config = docker_cli.create_host_config(
            port_bindings={80: 8080+i}
        )

        # Creating container
        start = time.time()
        container = docker_cli.create_container(image=name, host_config=host_config)
        end = time.time()

        create_array.append(end - start)

        active_containers.append(container.get("Id"))

        # Starting container
        start = time.time()
        docker_cli.start(container.get("Id"))
        end = time.time()

        start_array.append(end - start)

    log.info("Benchmark outputs:")
    log.info("Create stats:")
    for i in range(instances // 10):
        print(i, statistics.mean(create_array[i*10:(i+1)*10]))

    log.info("start stats")
    for i in range(instances // 10):
        print(i, statistics.mean(start_array[i*10:(i+1)*10]))

    if clean_flag:
        clean_containers(active_containers)