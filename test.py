import redis
import json
rds = redis.Redis(host='192.168.205.130', port=6379, db=13)


# print(rds.get())
for key in rds.keys():
    print(key.decode(), type(key.decode()))
    data_str = rds.get(key.decode()).decode()
    data = json.loads(data_str)
    print(data, type(data))
# io = psutil.disk_partitions()
# print(io)

