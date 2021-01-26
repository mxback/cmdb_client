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

from client import CmdbClient
import datetime, time
import redis
import json

rds = redis.Redis(host='192.168.205.130', port=6379, db=14)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        # client_data = {}
        client = CmdbClient()
        client_data = client.get_cpu['used']
        # client_data['memory'] = client.get_memory
        # client_data['disk'] = client.get_disk
        # client_data['start_time'] = client.get_start_time
        # client_data['hostname'] = client.get_hostname
        ip_address = client.get_ip_address
        # client_data['ip_address'] = ip_address
        # client_data['send_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # client_data['system'] = client.get_system
        client_data = json.dumps(client_data)
        print(client_data)
        rds.lpush(ip_address + "cpu:used", client_data)
        time.sleep(10)

