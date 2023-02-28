import os
import subprocess
from helpers.unikraft_helpers import _run_qemu


def _run_qemu_nographic(file_out, path, kernel_name, core, wait_to_complete=True):
    core_text = ""
    if core != -1:
        core_text = f"taskset {core}"

    command = f"""
        sudo {core_text} qemu-system-x86_64 -kernel "{kernel_name}" \
            -enable-kvm \
            -cpu host \
            -display none \
            -serial file:{file_out} > {file_out}.chrono
    """

    p = subprocess.Popen(command, shell=True, cwd=path)
    if wait_to_complete:
        p.wait()


def run_unikraft_boot_benchmark_instance(file_name):
    pwd = os.getcwd() + "/unikraft-images/"
    os.environ["UK_WORKDIR"] = pwd

    _run_qemu_nographic(
        file_out=f"../{file_name}",
        path=pwd,
        kernel_name="get_rdtsc_kvm-x86_64",
        core=-1,
        wait_to_complete=True,
    )


def run_unikraft_sqlite_benchmark_instance(file_name, core=-1):
    pwd = os.getcwd() + "/unikraft-images/"
    os.environ["UK_WORKDIR"] = pwd

    _run_qemu_nographic(
        file_out=f"../{file_name}",
        path=pwd,
        kernel_name="sqlite_kvm-x86_64",
        core=core,
        wait_to_complete=True,
    )


def run_unikraft_cpu_benchmark_instance(file_name, core, wait_to_complete):
    pwd = os.getcwd() + "/unikraft-images/"
    os.environ["UK_WORKDIR"] = pwd

    _run_qemu_nographic(
        file_out=f"../{file_name}",
        path=pwd,
        kernel_name="cpu_benchmark_kvm-x86_64",
        core=core,
        wait_to_complete=wait_to_complete,
    )
