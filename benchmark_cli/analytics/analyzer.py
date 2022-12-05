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
    "data-single.out.chrono",
    "data-200.out.chrono",
    "data-400.out.chrono",
    "data-600.out.chrono",
    "data-800.out.chrono",
    # "data-1000.out",
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
    "d_ng_s": SINGLE_FILES_LARGE,
    "d_ng_p": PARALLEL_FILES,
    "uk_ng_p": PARALLEL_FILES,
    "d_re_p": PARALLEL_FILES,
    "uk_re_p": PARALLEL_FILES,
    "d_re_s": SINGLE_FILES_LARGE,
    "uk_re_s": SINGLE_FILES,
    "uk_boot": SINGLE_FILES_LARGE,
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
    "200 Cont.",
    "400 Cont.",
    "600 Cont.",
    "800 Cont.",
    # "1000 Cont.",
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


def get_labels():
    labels = []
    for i in range(0, 101):
        labels.append(i)
    return labels


def get_data(experiment_name, runs, path):
    if experiment_name not in FILE_NAMES.keys():
        raise Exception("Experiment file definition not found")

    file_names = ["single"]
    for i in range(0, 100):
        file_names.append((i+1)*10)

    all_stats = []
    for file_name in file_names:
        current_stats = []
        for run in range(0, runs):
            current_stats.append(
                PARSER_TYPE[experiment_name](f"{path}/{experiment_name}/{run+1}-data-{file_name}.out")
            )
        all_stats.append(current_stats)

    return all_stats


def make_plot(data, experiment_name):
    # Build the plot
    fig, ax = plt.subplots()

    fig.set_figheight(5)
    fig.set_figwidth(9)

    data = np.array(data)
    means = np.mean(data, axis=1)

    means = means / means[0]
    std = np.mean(data, axis=1)
    means_d = np.mean(
        get_data("d_boot", 5, "../../raw-benchmark-files/data-all/benchmark-data"),
        axis=1
    )
    means_d = means_d / means_d[0]
    # std_d = np.std(
    #     get_data("d_boot", 5, "../../raw-benchmark-files/data/benchmark-data/d_boot"),
    #     axis=1
    # )

    # labels = FIGURE_LABELS[experiment_name]
    x_pos = np.arange(101)
    x_pos_2 = np.array([i*10+1 for i in range(0, 11)])
    x_pos_labels = [i * 100 + 1 for i in range(0, 11)]
    ax.plot(x_pos, means, label="Unikraft", color="orange")
    ax.plot(x_pos, means_d, label="Docker", color="blue")
    ax.legend()
    # ax.bar(x_pos, means,
    #        yerr=std,
    #        align='center',
    #        alpha=0.5,
    #        ecolor='black',
    #        capsize=5)
    ax.set_ylabel('Average boot time')
    ax.set_xticks(x_pos_2, x_pos_labels)
    # ax.set_xticklabels(labels)
    ax.set_title('Comparison between Docker and Unikraft on boot time benchmark (Normalized on first run)')
    ax.yaxis.grid(True)

    # Save the figure and show
    plt.tight_layout()
    EXP_NAME_COMB = "boot_normalized"
    plt.savefig(f"../figures/combined/{EXP_NAME_COMB}")
    print("done")


if __name__ == "__main__":
    exp_name = "uk_boot"
    data1 = get_data(exp_name, 5, f"../../raw-benchmark-files/data-all/benchmark-data")
    # data2 = get_data("uk_boot_chrono", 3, "../benchmark-data/uk_boot")

    print(data1)
    make_plot(data1, exp_name)
