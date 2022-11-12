import subprocess
import os


def run_docker_boot_benchmark(file_out):
    pwd = os.getcwd()
    command = f"./docker-bash-benchmark.sh > {file_out}"
    p = subprocess.Popen(command, shell=True, cwd=pwd)
    p.wait()
