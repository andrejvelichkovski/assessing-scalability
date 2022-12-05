import os


def get_mem_usage(file_name):
    os.system(
        f"free > {file_name}"
    )


def get_cpu_usage(file_name):
    # Measure CPU usage 5 times on 1 second intervals
    os.system(
        f"mpstat 1 5 > {file_name}"
    )


def measure_system_usage(path, run_index, instance):
    get_mem_usage(f"{path}/{run_index}-mem-{instance}.out")
    get_cpu_usage(f"{path}/{run_index}-cpu-{instance}.out")
