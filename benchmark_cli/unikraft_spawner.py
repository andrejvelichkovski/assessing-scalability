import click

from docker import APIClient

import logging as log
import statistics
import time

import os

import subprocess

from helpers.unikraft_helpers import run_unikraft

log.basicConfig(
    level=log.INFO, filename="/dev/stdout",
    format="%(levelname)s: %(message)s"
)

def setup_network(ips_required):
    subprocess.run("sudo ip link set dev virbr0 down", shell=True)
    subprocess.run("sudo ip link del dev virbr0", shell=True)

    subprocess.run("sudo ip link add virbr0 type bridge", shell=True)
    subprocess.run("tc qdisc add dev virbr0 root netem delay 0ms", shell=True)
    
    for i in range(ips_required):
        subprocess.run(f"sudo ip address add 172.{16 + i}.0.1/24 dev virbr0", shell=True)

    subprocess.run("sudo ip link set dev virbr0 up", shell=True)

def unikraft_spawner(instances, name):
    if instances % 10 != 0:
        log.error("Invalid Input: Please enter instances as number divisible by 10")
        exit()

    log.warning(f"Running this command will create {instances} Unikraft VMs without cleaning them!")

    INSTANCES_PER_IP = 200
    ips_required = (instances + INSTANCES_PER_IP - 1) // INSTANCES_PER_IP

    log.info(os.getcwd())


    setup_network(ips_required)
    active_vms = 0

    for i in range(ips_required):
        for j in range(INSTANCES_PER_IP):
            if active_vms == instances:
                break

            current_ip = f"172.{16 + i}.0.{2 + j}"
            run_unikraft(
                ip_address=current_ip,
                instance_cnt=active_vms+1,
                name=name,
            )
            active_vms += 1

            # Print benchmark progress
            if active_vms % (instances // 10) == 0:
                log.info(f"Benchmark progress: { (active_vms // (instances // 10)) * 10 }%")

if __name__ == '__main__':
    unikraft_spawner()