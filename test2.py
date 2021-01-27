import redis
import json
import pyecharts.options as opts
from pyecharts.charts import Line, Page, Grid

rds = redis.Redis(host='192.168.205.130', port=6379, db=14)

columns = []
cpu_usage_data = []
memory_usage_data = []
# print(rds.keys())
# key = "192.168.19.32"
key = "192.168.15.140"

for i in range(rds.llen(key)):
    columns.append(json.loads(rds.lrange(key, i, i)[0].decode())[2])
    cpu_usage_data.append(json.loads(rds.lrange(key, i, i)[0].decode())[0])
    memory_usage_data.append(json.loads(rds.lrange(key, i, i)[0].decode())[1])

columns = list(reversed(columns))
cpu_usage_data = list(reversed(cpu_usage_data))
memory_usage_data = list(reversed(memory_usage_data))

l1 = (
    Line(init_opts=opts.InitOpts(width="800px", height="400px"))
        .add_xaxis(xaxis_data=columns)
        .add_yaxis(
        series_name="CPU使用率",
        y_axis=cpu_usage_data,
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
        # 其他功能
        # toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        # X轴调整
        datazoom_opts=opts.DataZoomOpts(),
    )
)

l2 = (
    Line(init_opts=opts.InitOpts(width="800px", height="400px"))
        .add_xaxis(xaxis_data=columns)
        .add_yaxis(
        series_name="内存使用率",
        y_axis=memory_usage_data,
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
        title_opts=opts.TitleOpts(title="内存使用率(%)", subtitle="纯属虚构"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        # toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        # X轴调整
        datazoom_opts=opts.DataZoomOpts(),
    )
)

# grid = Grid()
# grid.add(l1, opts.GridOpts(pos_left="5%", pos_right="20%"), is_control_axis_index=True)
# grid.render("cpu.html")
page = Page()
page.add(l1)
page.add(l2)
page.render('usage.html')
