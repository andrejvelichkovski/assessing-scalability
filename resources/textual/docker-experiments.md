# Docker Benchmark Performance

This short document summarizes the performance of the Docker virtualization environment on a series of benchmarks.

### Evaluation details

All benchmarks have been run on the server. All experiments have been automated using Python scripts, and the 
`experiment_runner` CLI tool.

## Experiments performed

### Boot time microbenchmark

This benchmark measures the time required to boot a new Docker container. To provide good measurement details, RDTSC 
clock has been used.

We compare the boot time for a Docker container when running different number of sleeping containers in the background.

![](https://raw.githubusercontent.com/andrejvelichkovski/assessing-scalability/main/benchmark_cli/figures/d_boot.png?token=GHSAT0AAAAAABZA2QWHIR4PNX5DKFKQPI5CY3YVKZQ)

We can roughly see that the boot time almost doubles when 1000 Containers are running in the background.

This change in boot time can be easily noticed by trying to boot large number of containers in the same time. 
After booting some number of containers the process starts slowing down. This is also suggested by the graph we get 
above.

## Nginx performance

### Single server scalability measurements

The first Nginx benchmark measures how the performance of one server is affected by having a large number of servers 
running in the background.

All the background servers are running Nginx (on Docker)

![](https://raw.githubusercontent.com/andrejvelichkovski/assessing-scalability/main/benchmark_cli/figures/d_ng_s.png?token=GHSAT0AAAAAABZA2QWHCLX6BWKFVSWZTEXAY3YVL7A)

From the graph, we can notice that running sleeping containers in the background which don't do anything doesn't affect
the performance of the container we are benchmarking. This suggests that Nginx is easily scalable and adding more
containers doesn't affect the performance of the others.

### Parallel server scalability measurement

For the second experiment, we lunch 5 Docker Nginx instances and then benchmark them using 5 parallel clients.
This experiment has  the goal of testing whether the Input/Output share is fair between all sides.

![](https://raw.githubusercontent.com/andrejvelichkovski/assessing-scalability/main/benchmark_cli/figures/d_ng_p.png?token=GHSAT0AAAAAABZA2QWGHGLZLCZQEXUIXNTYY3YVLVQ)

From the graph, we can notice that the IO load is fairly split between all instances. This suggests that when adding new
containers, each of them will have fair access to the resources of the system.

## Redis performance

### Single server scalability measurements

Similarly like Nginx, we perform the same experiments for Redis. We launch one main Redis server (on Docker) which we
then test under different background load.

While for Nginx, the performance remained mainly stable between the benchmarks, Redis seems to be less scalable. Both
benchmarks using GET and SET request types seems to have performance drops when benchmarked under increased load.

![](https://raw.githubusercontent.com/andrejvelichkovski/assessing-scalability/main/benchmark_cli/figures/d_re_s.png?token=GHSAT0AAAAAABZA2QWGSSVHMA6VIPXZ6Q3AY3YVQTA)
![](https://raw.githubusercontent.com/andrejvelichkovski/assessing-scalability/main/benchmark_cli/figures/d_re_s_set.png?token=GHSAT0AAAAAABZA2QWHRFU3JAGUELHSGJLYY3YVQTA)

### Parallel server scalability measurements

The parallel benchmark performed in a similar way like the Nginx experiment gives similar results. This suggests that 
the IO load is fairly split between all clients and servers on the system.

![](https://raw.githubusercontent.com/andrejvelichkovski/assessing-scalability/main/benchmark_cli/figures/d_re_p.png?token=GHSAT0AAAAAABZA2QWGDO636DQ22NXYFVJ6Y3YVRDA)