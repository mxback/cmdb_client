from client import CmdbClient
import datetime, time
import redis
import json

rds = redis.Redis(host='192.168.205.130', port=6379, db=13)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        client_data = {}
        client = CmdbClient()
        client_data['cpu'] = client.get_cpu
        client_data['memory'] = client.get_memory
        client_data['disk'] = client.get_disk
        client_data['start_time'] = client.get_start_time
        client_data['hostname'] = client.get_hostname
        ip_address = client.get_ip_address
        client_data['ip_address'] = ip_address
        client_data['send_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client_data['system'] = client.get_system
        client_data = json.dumps(client_data)
        print(client_data)
        rds.set(ip_address, client_data)
        time.sleep(10)
