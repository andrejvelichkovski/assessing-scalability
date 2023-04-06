import subprocess

from docker import APIClient
import os

docker_cli = APIClient(base_url="unix:///run/docker.sock")


def create_container_taskset_static(taskset_text, image_name, tmpfs=""):
    core_val = taskset_text[8:]
    command = f"""
            sudo docker run -d --cpuset-cpus "{core_val}" {tmpfs} {image_name}
        """
    p = subprocess.Popen(command, shell=True)
    p.wait()


def create_container_taskset(port_in, port_out, taskset_text, image_name):
    core_val = taskset_text[8:]
    command = f"""
            sudo docker run -d --cpuset-cpus "{core_val}" -p {port_out}:{port_in} {image_name}
        """
    p = subprocess.Popen(command, shell=True)
    p.wait()


def create_container_static(image_name):
    container = docker_cli.create_container(image=image_name)
    return container


def create_container(port_in, port_out, image_name):
    host_config = docker_cli.create_host_config(
        port_bindings={port_in: port_out}
    )

    container = docker_cli.create_container(image=image_name, host_config=host_config)
    return container


def start_container(container):
    docker_cli.start(container.get("Id"))


def clean_all_containers():
    os.system("sudo docker kill $(sudo docker ps -q) > containers_killed.out")