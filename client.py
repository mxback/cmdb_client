import socket
import psutil
import datetime
import platform
import json

from psutil import net_if_addrs
import uuid


class CmdbClient(object):

    def __init__(self):
        self.cpu_data = {}
        self.mem_data = {}
        self.disk_data = {}
        self.start_time = ""
        self.ip = None

    @property
    def get_cpu(self):
        self.cpu_data['count'] = str(psutil.cpu_count())
        self.cpu_data['usage'] = str(psutil.cpu_percent(1))
        return self.cpu_data

    @property
    def get_memory(self):
        self.mem_data['total'] = str(int(psutil.virtual_memory().total / 1024 / 1024 / 1024))
        self.mem_data['used'] = str(int(psutil.virtual_memory().used / 1024 / 1024 / 1024))
        self.mem_data['free'] = str(int(psutil.virtual_memory().free / 1024 / 1024 / 1024))
        self.mem_data['usage'] = str(int(psutil.virtual_memory().used / 1024 / 1024 / 1024 * 100) // int(
            psutil.virtual_memory().total / 1024 / 1024 / 1024))
        return self.mem_data

    @property
    def get_disk(self):
        io = psutil.disk_partitions()
        for i in io:
            name = i.device.split(":")[0]
            self.disk_data[name] = {}
            try:
                o = psutil.disk_usage(i.mountpoint)
                self.disk_data[name]['total'] = str(int(o.total / (1024.0 * 1024.0 * 1024.0)))
                self.disk_data[name]['used'] = str(int(o.used / (1024 * 1024 * 1024)))
                self.disk_data[name]['free'] = str(int(o.free / (1024 * 1024 * 1024)))
                self.disk_data[name]['usage'] = str(
                    int(o.used / (1024 * 1024 * 1024) * 100) // int(o.total / (1024.0 * 1024.0 * 1024.0)))
            except PermissionError:
                self.disk_data[name]['total'] = None
                self.disk_data[name]['used'] = None
                self.disk_data[name]['free'] = None
                self.disk_data[name]['usage'] = None
        return self.disk_data

    @property
    def get_start_time(self):
        self.start_time = str(datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))
        return self.start_time

    @property
    def get_hostname(self):
        return socket.gethostname()

    @property
    def get_ip_address(self):
        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            soc.connect(('8.8.8.8', 80))
            self.ip = soc.getsockname()[0]
        finally:
            soc.close()
        return self.ip

    @property
    def get_system(self):
        return platform.system()


"""
    # 获取mac地址
    addr_num = hex(uuid.getnode())[2:]
    mac = "-".join(addr_num[i: i + 2] for i in range(0, len(addr_num), 2))
    print(mac)  # 4c-ed-fb-bb-e6-ac

    # 获取本机所有网卡的mac地址
    for k, v in net_if_addrs().items():
        for item in v:
            address = item[1]
            if "-" in address and len(address) == 17:
                print(address)
"""


class Monitor(object):
    def __init__(self, rds, client):
        self.rds = rds
        self.client = client
        self.client_data = []

    @property
    def push_usage(self):
        self.client_data.append(self.client.get_cpu['usage'])
        self.client_data.append(self.client.get_memory['usage'])
        self.client_data.append(datetime.datetime.now().strftime("%H:%M:%S"))
        client_data = json.dumps(self.client_data)
        if self.rds.llen(self.client.get_ip_address) >= 60:
            self.rds.rpop(self.client.get_ip_address)
        self.rds.lpush(self.client.get_ip_address, client_data)
        return client_data
