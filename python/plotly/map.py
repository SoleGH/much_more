import json
import os
import requests
# from plotly.graph_objs import Choropleth, Figure
from plotly import graph_objs as go


hubei_geo = "https://geojson.cn/api/china/1.6.2/420000.json"
file = "./hubei_geo.json"
rsp = requests.get(hubei_geo)
if not os.path.exists(file):
    with open(file, "w") as f:
        f.write(rsp.text)

with open(file, 'r') as f:
    geo_json = json.load(f)

locations = [item['properties']['name'] for item in geo_json['features']]
# ['武汉', '黄石', '十堰', '宜昌', '襄阳', '鄂州', '荆门', '孝感', '荆州', '黄冈', '咸宁', '随州', '恩施', '仙桃', '潜江', '天门', '神农架']
gdp_dict = {
    "武汉": 21106.23,
    "黄石": 2305.8,
    "十堰": 2565.8,
    "宜昌": 6191.12,
    "襄阳": 6102.41,
    "鄂州": 1341.3,
    "荆门": 2459.68,
    "孝感": 3258.54,
    "荆州": 3505.99,
    "黄冈": 3216.65,
    "咸宁": 1944.57,
    "随州": 1442.35,
    "恩施": 1661.36,
    "仙桃": 1125.13,
    "潜江": 951.97,
    "天门": 785.4,
    "神农架": 48.62,
}
values = [gdp_dict[i] for i in locations]

figure = go.Figure()
figure.add_trace(go.Choropleth(
    name="",
    geojson=hubei_geo,  # 指定地图数据包
    featureidkey="properties.name",
    locations=locations,
    z=values,
    marker=dict(
        line_color='lightgray',
        line_width=1
    ),
    showscale=False,
    autocolorscale=False,
    # colorscale=['#56DD58', '#5AE65D','#49BB4B','#3C993D','#2E7730'],  # 方式一: 给定颜色list
    colorscale=[[0, '#42DDDD'], [1 ,'#195555']],  # 方式二: 设置范围,只能设置两个颜色， 第一个元素设置起始颜色，第二个元素设置结束颜色
    # colorscale="Hot",  # 方式三: 使用预设值，Blackbody,Bluered,Blues,C ividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portl and,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd
))

# annotations = []
# for item, v in zip(locations, values):
#     # 注意：这里需要根据你的GeoJSON结构适配获取经纬度的方法
#     location_info = next(filter(lambda x: x['properties']['name'] == item, geo_json['features']))
#     lon_center, lat_center = location_info['properties']['center']  # center为中心点坐标

# 添加注解层
figure.add_trace(
    go.Scattergeo(
        geojson=hubei_geo,
        featureidkey="properties.name",
        locations=locations,
        text=[f"{locations[i]}: {values[i]}" for i in range(len(locations))],
        mode='text',
        textfont=dict(
            size=10,
            color='White'
        ),
        hoverinfo='none'  # 文本图层不需要悬停信息
    )
)

conf = dict(
    geo=dict(
        # scope="asia",  # ['africa', 'asia', 'europe', 'north america', 'south america', 'usa', 'world']
        showframe=True,  # 显示边框
        lataxis=dict(range=[29, 34]),  # 纬度范围
        lonaxis=dict(range=[105, 120]),  # 经度范围
        visible=False,  # Fasle为不显示背景地图

        # showrivers=False,  # 显示河流
        # showlakes=False   # 显示湖
    ),
    # # dragmode="select",
    # dragmode=False,
    # xaxis_visible=False,
    # plot_bgcolor="#FFFFFF",
    showlegend=True,
)

figure.update_layout(**conf)


figure.show()