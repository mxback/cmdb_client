import redis
import json
import pyecharts.options as opts
from pyecharts.charts import Line

rds = redis.Redis(host='192.168.205.130', port=6379, db=14)

columns = []
data = []
# print(rds.keys())
key = "192.168.19.32"

for i in range(rds.llen(key)):
    columns.append(json.loads(rds.lrange(key, i, i)[0].decode())[1])
    data.append(json.loads(rds.lrange(key, i, i)[0].decode())[0])

columns = list(reversed(columns))
data = list(reversed(data))

(
    Line(init_opts=opts.InitOpts(width="800px", height="400px"))
        .add_xaxis(xaxis_data=columns)
        .add_yaxis(
        series_name="CPU使用率",
        y_axis=data,
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
            ]
        ),
        markline_opts=opts.MarkLineOpts(
            data=[opts.MarkLineItem(type_="average", name="平均值")]
        ),
    )
        .set_global_opts(
        title_opts=opts.TitleOpts(title="CPU使用率(%)", subtitle="纯属虚构"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        # toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
    )
        .render("cpu.html")
)
