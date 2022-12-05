def get_wrk_benchmark_data(path):
    """
    Returns the throughput from the wrk benchmark
    """
    wrk_file = open(path, "r")
    content = wrk_file.readlines()

    for line in content:
        if "requests" not in line:
            continue
        return int(line.split()[0])


def get_redis_benchmark_data(path):
    """
    Returns the throughput from the redis-benchmark benchmark output
    """

    redis_bench_file = open(path, "r")
    content = redis_bench_file.readlines()

    benchmark_results = {}
    request_type = None
    for line in content:
        if "SET" in line:
            request_type = "SET"
        elif "GET" in line:
            request_type = "GET"

        if "requests per second" in line:
            benchmark_results[request_type] = float(line.split()[0])

    return benchmark_results["SET"]


def get_unikraft_boot_benchmark_data(path):
    uk_boot_file = open(path, "r")
    content = uk_boot_file.readlines()

    return int(content[-2])

def get_docker_boot_benchmark_data(path):
    docker_boot_file = open(path, "r")
    content = docker_boot_file.readlines()

    return int(content[1]) - int(content[0])


def get_chrono_benchmark_data(path):
    chrono_file = open(path, "r")
    content = chrono_file.readlines()

    return int(content[0])


if __name__ == "__main__":
    print(
        get_chrono_benchmark_data("../benchmark-data/uk_boot/1-data-single.out.chrono")
    )
