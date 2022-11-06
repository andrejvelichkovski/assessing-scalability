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

        if "throughput summary:" in line:
            benchmark_results[request_type] = float(line.split()[2])

    return benchmark_results["GET"]


if __name__ == "__main__":
    print(
        get_redis_benchmark_data("../benchmark-data/uk_re_p/1-data-0.out")
    )
