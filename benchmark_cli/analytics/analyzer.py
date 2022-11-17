from analytics.parser import get_wrk_benchmark_data, \
    get_redis_benchmark_data, \
    get_unikraft_boot_benchmark_data, \
    get_docker_boot_benchmark_data, \
    get_chrono_benchmark_data

import numpy as np
import matplotlib.pyplot as plt

PARALLEL_FILES = [
    "data-0.out",
    "data-1.out",
    "data-2.out",
    "data-3.out",
    "data-4.out",
]

SINGLE_FILES = [
    "data-single.out",
    "data-10.out",
    "data-20.out",
    "data-30.out",
    "data-40.out",
    "data-50.out",
]

SINGLE_FILES_LARGE = [
    "data-single.out",
    "data-50.out",
    "data-100.out",
    "data-150.out",
    "data-200.out",
    "data-250.out",
]

SINGLE_FILES_25 = [
    "data-single.out",
    "data-5.out",
    "data-10.out",
    "data-15.out",
    "data-20.out",
    "data-25.out",
]

SINGLE_FILES_25_CHRONO = [
    "data-single.out.chrono",
    "data-5.out.chrono",
    "data-10.out.chrono",
    "data-15.out.chrono",
    "data-20.out.chrono",
    "data-25.out.chrono",
]

FILE_NAMES = {
    "uk_ng_s": SINGLE_FILES,
    "d_ng_s": SINGLE_FILES,
    "d_ng_p": PARALLEL_FILES,
    "uk_ng_p": PARALLEL_FILES,
    "d_re_p": PARALLEL_FILES,
    "uk_re_p": PARALLEL_FILES,
    "d_re_s": SINGLE_FILES,
    "uk_re_s": SINGLE_FILES,
    "uk_boot": SINGLE_FILES_25,
    "d_boot": SINGLE_FILES_LARGE,
    "uk_boot_chrono": SINGLE_FILES_25_CHRONO,
}

PARSER_TYPE = {
    "d_ng_p": get_wrk_benchmark_data,
    "uk_ng_p": get_wrk_benchmark_data,
    "d_ng_s": get_wrk_benchmark_data,
    "uk_ng_s": get_wrk_benchmark_data,
    "d_re_p": get_redis_benchmark_data,
    "uk_re_p": get_redis_benchmark_data,
    "d_re_s": get_redis_benchmark_data,
    "uk_re_s": get_redis_benchmark_data,
    "uk_boot": get_unikraft_boot_benchmark_data,
    "d_boot": get_docker_boot_benchmark_data,
    "uk_boot_chrono": get_chrono_benchmark_data,
}

SINGLE_BENCHMARK_LABELS = [
    "Single",
    "10 VMs",
    "20 VMs",
    "30 VMs",
    "40 VMs",
    "50 VMs",
]

PARALLEL_BENCHMARK_LABELS = [
    "Instance #1",
    "Instance #2",
    "Instance #3",
    "Instance #4",
    "Instance #5",
]

FIGURE_LABELS = {
    "d_ng_p": PARALLEL_BENCHMARK_LABELS,
    "uk_ng_p": PARALLEL_BENCHMARK_LABELS,
    "d_ng_s": SINGLE_BENCHMARK_LABELS,
    "uk_ng_s": SINGLE_BENCHMARK_LABELS,
    "d_re_p": PARALLEL_BENCHMARK_LABELS,
    "uk_re_p": PARALLEL_BENCHMARK_LABELS,
    "uk_re_s": SINGLE_BENCHMARK_LABELS,
    "d_re_s": SINGLE_BENCHMARK_LABELS,
    "uk_boot": SINGLE_BENCHMARK_LABELS,
    "d_boot": SINGLE_BENCHMARK_LABELS,
}


def get_data(experiment_name, runs, path):
    if experiment_name not in FILE_NAMES.keys():
        raise Exception("Experiment file definition not found")

    all_stats = []
    for file_name in FILE_NAMES[experiment_name]:
        current_stats = []
        for run in range(0, runs):
            current_stats.append(
                PARSER_TYPE[experiment_name](f"{path}/{run+1}-{file_name}")
            )
        all_stats.append(current_stats)

    return all_stats


def make_plot(data, experiment_name):
    # Build the plot
    fig, ax = plt.subplots()

    fig.set_figheight(5)
    fig.set_figwidth(8)

    data = np.array(data)
    means = np.mean(data, axis=1)
    std = np.std(data, axis=1)

    labels = FIGURE_LABELS[experiment_name]
    x_pos = np.arange(len(labels))

    ax.bar(x_pos, means,
           yerr=std,
           align='center',
           alpha=0.5,
           ecolor='black',
           capsize=5)
    ax.set_ylabel('Average wrk performance')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels)
    ax.set_title('Comparison how docker performs under more active nginx containers')
    ax.yaxis.grid(True)

    # Save the figure and show
    plt.tight_layout()
    plt.savefig(f"../figures/{experiment_name}")
    print("done")


def make_plot_double(data1, data2, experiment_name):
    # Build the plot
    fig, ax = plt.subplots()

    fig.set_figheight(5)
    fig.set_figwidth(8)

    data1= np.array(data1)
    means1 = np.mean(data1, axis=1)
    std1 = np.std(data1, axis=1)

    data2 = np.array(data2)
    means2 = np.mean(data2, axis=1)
    std2 = np.std(data2, axis=1)

    labels = FIGURE_LABELS[experiment_name]
    x_pos = np.arange(len(labels))

    BAR_WIDTH = 0.35

    ax.bar(x_pos, means1,
           yerr=std1,
           align='center',
           alpha=0.5,
           ecolor='black',
           capsize=5)
    ax.bar(x_pos+BAR_WIDTH, means2,
           yerr=std2,
           align='center',
           alpha=0.5,
           ecolor='black',
           capsize=5)


    ax.set_ylabel('Average wrk performance')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels)
    ax.set_title('Comparison how docker performs under more active nginx containers')
    ax.yaxis.grid(True)

    # Save the figure and show
    plt.tight_layout()
    plt.savefig(f"../figures/{experiment_name}")
    print("done")



if __name__ == "__main__":
    exp_name = "uk_boot"
    data1 = get_data(exp_name, 3, f"../benchmark-data/{exp_name}")
    data2 = get_data("uk_boot_chrono", 3, "../benchmark-data/uk_boot")

    print(data1)
    print(data2)
    make_plot(data1, exp_name)
