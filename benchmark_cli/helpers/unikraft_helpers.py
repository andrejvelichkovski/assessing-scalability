import os
import subprocess


def setup_network(ips_required):
    p = subprocess.run("sudo ip link set dev virbr0 down", shell=True)
    p.wait()

    p = subprocess.run("sudo ip link del dev virbr0", shell=True)
    p.wait()

    p = subprocess.run("sudo ip link add virbr0 type bridge", shell=True)
    p.wait()
    # subprocess.run("tc qdisc add dev virbr0 root netem delay 0ms", shell=True)

    for i in range(ips_required):
        p = subprocess.run(f"sudo ip address add 172.{16 + i}.0.1/24 dev virbr0", shell=True)
        p.wait()

    p = subprocess.run("sudo ip link set dev virbr0 up", shell=True)
    p.wait()

def _run_qemu(daemonize, display_option, path, kernel_name):
    command = f"""
        sudo qemu-system-x86_64 -kernel "{kernel_name}" \
            -enable-kvm \
            -cpu host \
            -daemonize \
            {display_option} \
    """

    p = subprocess.Popen(command, shell=True, cwd=path)
    p.wait()


def _run_qemu_network(instance_cnt, ip_address, path, kernel_name, conf_file=""):
    mac_address_unformated = hex(instance_cnt)[2:].zfill(12)
    mac_address = ":".join(
        [mac_address_unformated[i * 2:(i + 1) * 2] for i in range(6)]
    )

    command = f"""
        sudo qemu-system-x86_64 -fsdev local,id=myid,path=$(pwd)/fs0,security_model=none \
            -device virtio-9p-pci,fsdev=myid,mount_tag=fs0,disable-modern=on,disable-legacy=off \
            -netdev bridge,id=en0,br=virbr0 \
            -device virtio-net-pci,netdev=en0,mac={mac_address} \
            -kernel "{kernel_name}" \
            -append "-M 20 netdev.ipv4_addr={ip_address} netdev.ipv4_gw_addr=172.16.0.1 netdev.ipv4_subnet_mask=255.255.255.0 -- {conf_file}" \
            -cpu host \
            -enable-kvm \
            -daemonize \
            -display none
    """
    p = subprocess.Popen(command, shell=True, cwd=path)
    p.wait()


def _prepare_redis_conf_file(ip_address, instance_cnt):
    conf_file = open(f"./unikraft-redis/apps/app-redis/fs0/redis{instance_cnt}.conf", "w")
    conf_file.write(f"bind {ip_address}\n")
    conf_file.write("port 6379\n")
    conf_file.write("tcp-backlog 511\n")
    conf_file.write("timeout 0\n")
    conf_file.write("tcp-keepalive 300\n")
    conf_file.close()


def _run_redis_instance(ip_address, instance_cnt):
    pwd = os.getcwd()
    redis_pwd = pwd + "/unikraft-redis/apps/app-redis"
    os.environ["UK_WORKDIR"] = redis_pwd + "/../../"

    _prepare_redis_conf_file(ip_address, instance_cnt)

    _run_qemu_network(
        instance_cnt=instance_cnt,
        ip_address=ip_address,
        path=redis_pwd,
        kernel_name="build/redis_kvm-x86_64",
        conf_file=f"/redis{instance_cnt}.conf",
    )

def _run_nginx_instance(ip_address, instance_cnt):
    pwd = os.getcwd()
    nginx_pwd = pwd + "/unikraft-nginx/apps/app-nginx"
    os.environ["UK_WORKDIR"] = nginx_pwd + "/../../"

    _run_qemu_network(
        instance_cnt=instance_cnt,
        ip_address=ip_address,
        path=nginx_pwd,
        kernel_name="build/nginx_kvm-x86_64",
    )


def _run_sleeping_instance():
    pwd = os.getcwd() + "/unikraft-sleeping/"
    os.environ["UK_WORKDIR"] = pwd

    _run_qemu(
        daemonize=True,
        display_option="-display none",
        path=pwd,
        kernel_name="build/helloworld_kvm-x86_64",
    )


def run_unikraft(ip_address, instance_cnt, name):
    if name == "nginx":
        _run_nginx_instance(ip_address, instance_cnt)
    elif name == "redis":
        _run_redis_instance(ip_address, instance_cnt)
    elif name == "sleeping":
        _run_sleeping_instance()


def clean_all_vms():
    os.system("ps -ef | grep qemu-system-x86_64 | grep -o ^[a-z[:space:]]*[0-9]* | grep -o [0-9]* > kernels")
    os.system("sudo kill `cat kernels`")
