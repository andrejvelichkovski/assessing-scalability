# Benchmark CLIs

The CLIs in this category will be used to benchmark the performance of Docker and Unikraft.

Currently, only one CLI is available, however as the work progresses, more CLI tools will be added.

## Setting up the environment

1. Make sure python3 is installed.
2. Make sure pip3 is installed.
3. Install all the CLI dependencies using: `pip3 install -r requirements.txt`

### Creating virtual environment [Optional]

Before executing step 3, it is highly recommended to create a new virtual environment, using the steps below:

1. Install venv using: `pip3 install venv`
2. Create a new virtual environment: `virtualenv <venv-name>`
3. Activate the new virtual env: `. <venv-name>/bin/activate`

## Using Spawner CLI

The `spawner.py` CLI automatically creates and starts containers/VMs to make the process of benchmarking easier.

Usage:
```
python3 spawner.py --instances X --name Y [command] [command specific options]
```

### Docker Spawner

Optional flags:
* `--clean_flag` to skip the cleaning process at the end once all images are created
