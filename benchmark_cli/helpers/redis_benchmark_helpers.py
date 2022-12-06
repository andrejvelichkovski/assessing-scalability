import subprocess


def run_redis_benchmark(host, port, file_out):
    p = subprocess.Popen(
        f"redis-benchmark -n 10000000 -t set,get -c 30 -P 16 -h {host} -p {port} > {file_out}",
        shell=True,
    )
    p.wait()
