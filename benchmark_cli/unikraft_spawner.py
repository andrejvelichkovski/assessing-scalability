import click

from docker import APIClient

import logging as log
import statistics
import time

import os

import subprocess

log.basicConfig(
    level=log.INFO, filename="/dev/stdout",
    format="%(levelname)s: %(message)s"
)

def setup_network(ips_required):
    subprocess.run("sudo ip link set dev virbr0 down", shell=True)
    subprocess.run("sudo ip link del dev virbr0", shell=True)

    subprocess.run("sudo ip link add virbr0 type bridge", shell=True)
    for i in range(ips_required):
        subprocess.run(f"sudo ip address add 172.{16 + i}.0.1/24 dev virbr0", shell=True)

    subprocess.run("sudo ip link set dev virbr0 up", shell=True)

def run_single_instance(ip_address):
    pwd_path = "/home/andrej/assessing-scalability/benchmark_cli/unikraft-nginx/apps/app-nginx"
    os.environ["UK_WORKDIR"] = pwd_path + "/../../"

    command = f"""
        sudo qemu-system-x86_64 -fsdev local,id=myid,path=$(pwd)/fs0,security_model=none \
            -device virtio-9p-pci,fsdev=myid,mount_tag=fs0,disable-modern=on,disable-legacy=off \
            -netdev bridge,id=en0,br=virbr0 \
            -device virtio-net-pci,netdev=en0 \
            -kernel "build/nginx_kvm-x86_64" \
            -append "-M 1024 netdev.ipv4_addr={ip_address} netdev.ipv4_gw_addr=172.16.0.1 netdev.ipv4_subnet_mask=255.255.0.0 --" \
            -cpu host \
            -enable-kvm \
            -daemonize \
            -display none
    """

    p = subprocess.Popen(command, shell=True, cwd=pwd_path)
    
def unikraft_spawner(instances, name):
    if instances % 10 != 0:
        log.error("Invalid Input: Please enter instances as number divisible by 10")
        exit()

    log.warning(f"Running this command will create {instances} Unikraft VMs without cleaning them!")

    INSTANCES_PER_IP = 200
    ips_required = (instances + INSTANCES_PER_IP - 1) // INSTANCES_PER_IP

    setup_network(ips_required)


    active_vms = 0

    for i in range(ips_required):
        for j in range(INSTANCES_PER_IP):
            if active_vms == instances:
                break

            current_ip = f"172.{16 + i}.0.{2 + j}"
            run_single_instance(current_ip)
            active_vms += 1

            # Print benchmark progress
            if active_vms % (instances // 10) == 0:
                log.info(f"Benchmark progress: { (active_vms // (instances // 10)) * 10 }%")


if __name__ == '__main__':
    unikraft_spawner()