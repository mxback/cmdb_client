import redis
import json
import pyecharts.options as opts
from pyecharts.charts import Line, Page, Grid

rds = redis.Redis(host='192.168.205.130', port=6379, db=14)
keys = rds.keys()
# print(rds.keys())
key = "192.168.15.140"

if key.encode() in keys:
    print('a')
