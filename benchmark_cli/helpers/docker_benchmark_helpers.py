import subprocess
import os


def run_docker_boot_benchmark(file_out):
    pwd = os.getcwd()
    command = f"./docker-bash-benchmark.sh > {file_out}"
    p = subprocess.Popen(command, shell=True, cwd=pwd)
    p.wait()


def run_docker_cpu_benchmark(file_name, core, wait_to_complete):
    pwd = os.getcwd()

    core_text = ""
    if core != -1:
        core_text = f"taskset {core}"

    command = f"sudo {core_text} docker run cpu-benchmark > {file_name}"
    p = subprocess.Popen(command, shell=True, cwd=pwd)

    if wait_to_complete:
        p.wait()
