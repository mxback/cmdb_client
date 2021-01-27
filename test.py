# import redis
# import json
# rds = redis.Redis(host='192.168.205.130', port=6379, db=13)
#
#
# # print(rds.get())
# for key in rds.keys():
#     print(key.decode(), type(key.decode()))
#     data_str = rds.get(key.decode()).decode()
#     data = json.loads(data_str)
#     print(data, type(data))
# # io = psutil.disk_partitions()
# # print(io)

from client import CmdbClient, Monitor
import datetime, time
import redis
import json

rds = redis.Redis(host='192.168.205.130', port=6379, db=14)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    while True:
        client = CmdbClient()
        monitor = Monitor(rds, client)
        monitor.push_usage
        # client_data = []
        # client = CmdbClient()
        # client_data.append(client.get_cpu['usage'])
        # client_data.append(client.get_memory['usage'])
        # ip_address = client.get_ip_address
        # client_data.append(datetime.datetime.now().strftime("%H:%M:%S"))
        # client_data = json.dumps(client_data)
        # print(client_data)
        # if rds.llen(ip_address) >= 60:
        #     rds.rpop(ip_address)
        # rds.lpush(ip_address, client_data)
        time.sleep(1)
