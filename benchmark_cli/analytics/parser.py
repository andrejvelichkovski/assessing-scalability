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


if __name__ == "__main__":
    get_wrk_benchmark_data("../benchmark-data/uk_ng_s-1-data-10.out")