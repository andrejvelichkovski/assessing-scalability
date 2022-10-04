# Assessing the Scalability of Lightweight Virtualisation Systems

Assessing the Scalability of Lightweight Virtualisation Systems is [my](https://github.com/andrejvelichkovski) final year university project under the supervision of [Dr. Pierre Olivier](https://sites.google.com/view/pierreolivier/) at the [Department of Computer Science, University of Manchester](https://cs.manchester.ac.uk).

This repository will contain all the implementation files and the documents used as part of this project.

## Key focus

As part of this study, two lightweight virtualization systems will be used:
1. [Docker](https://www.docker.com) - highly popular containerization tool
2. [Unikraft](https://unikraft.org) - new open-source Unikernel Development Tool

Different benchmarks will be run using these technologies, to assess how scalable both tools are.

## Benchmarks

There will be three types of benchmarks performed:
1. Network intensive benchmarks
2. Storage intensive benchmarks
3. Compute/memory intensive benchmakrks

### Network intensive benchmarks

To asses how well the systems scale with network intensive applications, [Redis](https://redis.io) (with [redis-benchmark](https://redis.io/docs/reference/optimization/benchmarks/)) and [Nginx](https://www.nginx.com) (with [ApacheBench](https://httpd.apache.org/docs/2.4/programs/ab.html) or [wrk](https://github.com/wg/wrk)) will be used

### Storage intensive benchmarks

For testing how well these systems perform with storage intensive applications, we plan to use:
* [SQLite](https://www.sqlite.org/index.html)
* [fio](https://fio.readthedocs.io/en/latest/fio_doc.html)

### Compute/memory intensive benchmarks

As part of this benchmark part, we plan to use:
* [NAS Parallel Benchmarks](https://www.nas.nasa.gov/software/npb.html) in either single-threaded or multi-threaded fashion
* [STREAM benchmark](https://www.cs.virginia.edu/stream/)
