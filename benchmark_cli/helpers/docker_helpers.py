from docker import APIClient
import os

docker_cli = APIClient(base_url="unix:///run/docker.sock")

def create_container(port, image_name):
    host_config = docker_cli.create_host_config(
        port_bindings={80: port}
    )

    container = docker_cli.create_container(image=image_name, host_config=host_config)
    return container

def start_container(container):
    docker_cli.start(container.get("Id"))

def clean_all_containers():
    os.system("sudo docker kill $(sudo docker ps -q) > containers_killed.out")