import os
import subprocess
import time

PARAMETERS = "-d 20s -c 30 -t 14"

def run_wrk_benchmark(file_data, ip_address):
    os.system(
        f"wrk {PARAMETERS} http://{ip_address}/ > {file_data}"
    )


def get_wrk_benchmark_process(file_data, ip_address):
    p = subprocess.Popen(
        f"wrk {PARAMETERS} http://{ip_address} > {file_data}",
        shell=True,
    )
    return p


def network_stress_attacker(sleep_time, ip_address):
    p = subprocess.Popen(
        f"while true; do curl -s http://{ip_address} > /dev/null; done;",
        shell=True,
    )
    time.sleep(sleep_time)
    p.kill()
