#!/bin/bash

sudo apt-get install docker

cd ~/assessing-scalability/resources/docker_images/boot-benchmark/ || exit
sudo docker image build -t boot-benchmark .

cd ~/assessing-scalability/resources/docker_images/sleep-container/ || exit
sudo docker image build -t sleep-container .

cd ~/assessing-scalability/resources/docker_images/nginx/ || exit
sudo docker image build -t nginx-benchmark .

cd ~/assessing-scalability/resources/docker_images/redis/ || exit
sudo docker image build -t redis-benchmark .