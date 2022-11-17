#!/bin/bash

# Preparing chrono time measurements
cd ~/assessing-scalability/benchmark_cli/ || exit
git clone https://github.com/olivierpierre/chrono.git

cd ~/assessing-scalability/benchmark_cli/chrono || echo "FAILED"
make
