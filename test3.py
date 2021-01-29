import redis
import json
import pyecharts.options as opts
from pyecharts.charts import Line, Page, Grid

rds = redis.Redis(host='192.168.205.130', port=6379, db=14)
keys = rds.keys()
# print(rds.keys())
key = "192.168.15.140"


# if key.encode() in keys:
#     print('a')


class HostUsageInfo(object):

    def __init__(self):
        self.columns = []
        self.cpu_usage_data = []
        self.memory_usage_data = []

    def host_usage_data(self, rds, key):
        for i in range(rds.llen(key)):
            self.columns.append(json.loads(rds.lrange(key, i, i)[0].decode())[2])
            self.cpu_usage_data.append(json.loads(rds.lrange(key, i, i)[0].decode())[0])
            self.memory_usage_data.append(json.loads(rds.lrange(key, i, i)[0].decode())[1])
        return self.columns, self.cpu_usage_data, self.memory_usage_data

    @classmethod
    def get_usage_data(cls, rds, key):
        columns, cpu_usage_data, memory_usage_data = cls().host_usage_data(rds, key)
        return list(reversed(columns)), list(reversed(cpu_usage_data)), list(reversed(memory_usage_data))


a, b, c = HostUsageInfo.get_usage_data(rds, key)
print(a, b, c)
