from analytics.parser import get_wrk_benchmark_data

import numpy as np
import matplotlib.pyplot as plt

FILE_NAMES = {
    "uk_ng_s": [
        "data-single.out",
        "data-50.out",
        "data-100.out",
        "data-150.out",
        "data-200.out",
        "data-250.out",
    ],
    "d_ng_s": [
        "data-single.out",
        "data-50.out",
        "data-100.out",
        "data-150.out",
        "data-200.out",
        "data-250.out",
    ],
    "d_ng_p": [
        "data-0.out",
        "data-1.out",
        "data-2.out",
        "data-3.out",
        "data-4.out",
    ],
    "uk_ng_p": [
        "data-0.out",
        "data-1.out",
        "data-2.out",
        "data-3.out",
        "data-4.out",
    ]
}


def get_data(experiment_name, runs, path):
    if experiment_name not in FILE_NAMES.keys():
        raise Exception("Experiment file definition not found")

    all_stats = []
    for file_name in FILE_NAMES[experiment_name]:
        current_stats = []
        for run in range(0, runs):
            current_stats.append(
                get_wrk_benchmark_data(f"{path}/{run+1}-{file_name}")
            )
        all_stats.append(current_stats)

    return all_stats


def make_plot(data, file_name):
    # Build the plot
    fig, ax = plt.subplots()

    fig.set_figheight(5)
    fig.set_figwidth(8)

    data = np.array(data)
    means = np.mean(data, axis=1)
    std = np.std(data, axis=1)

    labels = [
        'Single',
        '50 instances',
        '100 instances',
        '150 instances',
        '200 instances',
        '250 instances'
    ]
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
    # ax.yaxis.grid(True)

    # Save the figure and show
    plt.tight_layout()
    plt.savefig(f"../figures/{file_name}")
    print("done")


if __name__ == "__main__":
    data = get_data("d_ng_p", 1, "../benchmark-data/d_ng_p")
    make_plot(data, "d_ng_p")
