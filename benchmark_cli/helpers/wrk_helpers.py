import os


def run_wrk_benchmark(file_data, ip_address):
    os.system(
        f"wrk -d 10s -c 30 -t 14 http://{ip_address}/ > {file_data}"
    )
