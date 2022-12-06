import os
import subprocess
from helpers.unikraft_helpers import _run_qemu


def _run_qemu_nographic(file_out, path, kernel_name):
    command = f"""
        ../chrono/chronoquiet sudo qemu-system-x86_64 -kernel "{kernel_name}" \
            -enable-kvm \
            -cpu host \
            -display none \
            -serial file:{file_out} > {file_out}.chrono
    """

    p = subprocess.Popen(command, shell=True, cwd=path)
    p.wait()


def run_unikraft_boot_benchmark_instance(file_name):
    pwd = os.getcwd() + "/unikraft-images/"
    os.environ["UK_WORKDIR"] = pwd

    _run_qemu_nographic(
        file_out=f"../{file_name}",
        path=pwd,
        kernel_name="get_rdtsc_kvm-x86_64",
    )
