#!/bin/bash
./rdtsc_helpers/get_rdtsc
echo ""
sudo docker run boot-benchmark 
