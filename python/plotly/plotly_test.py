#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/11 16:32
# @Author  : Scott Yang
# @Site    :
# @File    : plotly.py
# @Software: PyCharm
import copy
import json
import time

import numpy
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# import requests


class TestPlotly:
    """
    pip install plotly==5.15.0
    """

    def get_df(self, group: bool = False):
        color_list = ["#E3A249", "#3D4EE3", "#96941A", "#E3E032"]

        color_map = {"g1": "#E3A249", "g2": "#E3E032"}

        if group:
            db0 = {"x": [23, 34, 45, 12, 34, 33,56, 34, 56, 45, 23, 33],
                   "y": [34, 23, 12, 45, 45, 33,56, 23, 34, 45, 23, 33],
                   # "name": ['g1', 'g1', 'g1', 'g1', 'g1', 'g1', 'g2', 'g2', 'g2', 'g2', 'g2', 'g2']
                   "name": ['g1', 'g1', 'g1', 'g1', 'g1', 'g1', 'g1', 'g1', 'g1', 'g1', 'g1', 'g1']
                   }
            # return dict(g1=pd.DataFrame(db0), g2=pd.DataFrame(db1)), color_map
            return pd.DataFrame(db0), color_map
        else:
            db = {
                "x": [1, 2, 3, 4, 5],
                "y": [1, 2, 3, 4, 5],
                "name": ["g1", "g1", "g1", "g2", "g2"],
            }
            return pd.DataFrame(db), color_map

    def get_trendline(self, x: list, y: list):
        if x and y:
            p = numpy.polyfit(x, y, 1)
            # trendline = {"base": p[-1], "slope": p[-2]}
            base = p[-1]
            slope = p[-2]
        else:
            base = 0
            slope = 0

        y = lambda x: x * slope + base

        return (min(x), y(min(x))), (max(x), y(max(x)))

    def test_scatter_plots(self):
        group = True
        df, color_map = self.get_df(group)
        group_order = ["g2", "g1"]
        if group:
            fig = go.Figure()
            # for name, df in df.items():
            #     fig.add_trace(go.Scatter(x=df["x"], y=df['y'], name=name, marker_color=color_map[name]))

            # fig.add_trace(go.Scatter(x=df["g2"]["x"], y=df["g2"]['y'], name="g2", marker_color=color_map["g2"]))
            # fig.add_trace(go.Scatter(x=df["g1"]["x"], y=df["g1"]['y'], name="g1", marker_color=color_map["g1"]))

            for name in group_order:
                c_df = df[df["name"] == name]
                fig.add_trace(
                    go.Scatter(
                        x=c_df["x"],
                        y=c_df["y"],
                        # x=[],
                        # y=[],
                        name=name,
                        mode="markers",
                        marker_color=color_map[name],
                    )
                )
            (x0, y0), (x1, y1) = self.get_trendline(list(df["x"]), list(df["y"]))
            # fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], line_shape='spline', name="Trendline", mode='lines'))
        else:
            fig = px.scatter(
                df,
                color="name",
                x="x",
                y="y",
                trendline="ols",
                color_discrete_map=color_map,
            )

        # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Layout.html#id3
        fig.update_layout(
            title="test title",
            plot_bgcolor="#FFFFFF",
            showlegend=True,
            legend=dict(
                x=0.9,
                y=0.05,
                # bgcolor="#E5ECF6",
                title="",
                bgcolor="rgba(0, 0, 0, 0)",
                font=dict(size=20),
            ),
            xaxis=dict(
                # tick0=  # set first tick
                dtick=1,  # set step
                title=dict(text="xtitle", font=dict(size=23)),
                gridcolor="#E5ECF6",
                linecolor="#E5ECF6",
                linewidth=2,
                tickfont=dict(size=20),
                range=(23.5, 40),
            ),
            yaxis=dict(
                dtick=2,
                title=dict(text="y title", font=dict(size=23)),
                gridcolor="#E5ECF6",
                linecolor="#E5ECF6",
                linewidth=2,
                tickfont=dict(size=20),
            ),
        )
        fig.update_traces(marker=dict(symbol="circle", size=10))

        fig.show()

        new_fig = copy.copy(fig)
        new_fig.update_layout(
            showlegend=False,
            title=None,
            xaxis_visible=False,
            yaxis_visible=False
        )
        fig.show()
        new_fig.show()


def test_timeline():
    # df = pd.DataFrame([
    #     dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28'),
    #     dict(Task="Job A", Start='2009-03-05', Finish='2009-04-15'),
    #     dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30')
    # ])
    df = pd.DataFrame(
        [
            dict(Task="Adidas", Start=57, Finish=60),
            # dict(Task="Adidas", Start=61, Finish=66),
            # dict(Task="Adidas", Start=67, Finish=72),
            # dict(Task="Adidas", Start=73, Finish=78),
            # dict(Task="Adidas", Start=79, Finish=85),
            # dict(Task="Adidas", Start=86, Finish=94),
            dict(Task="Adidas", Start=95, Finish=104),
            dict(Task="Aigle", Start=62, Finish=70),
            # dict(Task="Aigle", Start=71, Finish=79),
            # dict(Task="Aigle", Start=80, Finish=89),
            dict(Task="Aigle", Start=90, Finish=102),
        ]
    )
    # df["Start"] = df["Start"] * 1000 * 600
    # df["Finish"] = df["Finish"] * 1000 * 600

    # fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", range_x=(50, 110))
    fig.update_yaxes(
        autorange="reversed"
    )  # otherwise tasks are listed from the bottom up

    # fig.update_layout(
    #     title="test title",
    #     plot_bgcolor="#FFFFFF",
    #     legend=dict(
    #         x=0.9,
    #         y=0.05,
    #         # bgcolor="#E5ECF6",
    #         title="",
    #         bgcolor="rgba(0, 0, 0, 0)",
    #         font=dict(size=20),
    #     ),
    #     xaxis=dict(
    #         # tick0=  # set first tick
    #         dtick=4,  # set step
    #         title=dict(text="xtitle", font=dict(size=23)),
    #         gridcolor="#E5ECF6",
    #         linecolor="#E5ECF6",
    #         linewidth=2,
    #         tickfont=dict(size=20),
    #         range=(50, 110),
    #     ),
    # )
    fig.show()


color = {"client": "#6B8CA4", "competitor": "#8CA4B4", "core_bg": "#B4C5D1"}


def add_single_trace(fig, df, is_client: bool = False, **kwargs):
    brands = list(set(df["brand"]))
    for brand in brands:
        brand_df = df[df["brand"] == brand]
        config = dict(
            x=brand_df["min"],
            y=brand_df["brand"],
            mode="markers+text",
            text=df["name"],
            hovertemplate="(%{x},)",
            name=brand,
            marker=dict(
                symbol="circle",
                size=30,
                color=color["client"] if is_client else color["competitor"],
            ),
            # offsetgroup=brand,
        )
        if kwargs:
            config.update(**kwargs)

        fig.add_trace(go.Scatter(**config))


def add_demo(fig, core_x0, core_x1, df):
    demo_width = 30

    min_x = min(df["min"])

    if core_x0 - min_x > demo_width:
        demo_start = min_x
    else:
        demo_start = core_x1 + 2

    add_single_trace(
        fig,
        pd.DataFrame([dict(brand="", min=demo_start + 7, max=demo_start + 8, name="")]),
        texttemplate=" Interval, e.g.20-30cm",
        textposition="middle right",
        mode="markers+text",
        hoverinfo="none",
        hovertemplate=None,
        marker_size=20,
        marker_symbol="square"
    )

    add_single_trace(
        fig,
        pd.DataFrame([dict(brand="", min=demo_start, max=demo_start, name="")]),
        texttemplate=" Single. e.g.16cm",
        textposition="middle right",
        mode="markers+text",
        hoverinfo="none",
        hovertemplate=None,
        marker_size=20,
    )


def customer_bar():
    fig = go.Figure()
    df = pd.DataFrame(
        [
            dict(brand="Adidas", min=57, max=60, name="XS"),
            dict(brand="Adidas", min=61, max=66, name="L"),
            dict(brand="Adidas", min=67, max=72, name="XS"),
            dict(brand="Adidas", min=73, max=78, name="XS"),
            dict(brand="Adidas", min=79, max=85, name="XS"),
            dict(brand="Adidas", min=86, max=94, name="XS"),
            dict(brand="Adidas", min=95, max=104, name="XS"),
            dict(brand="Adidas", min=105, max=105, name="XS"),
            dict(brand="Aigle", min=62, max=70, name="XS"),
            dict(brand="Aigle", min=71, max=79, name="XS"),
            dict(brand="Aigle", min=80, max=89, name="XS"),
            dict(brand="Aigle", min=90, max=102, name="XS"),
        ]
    )

    core_x0 = 57
    core_x1 = 60
    add_demo(fig, core_x0, core_x1, df)

    # add highlight
    highlight_shape = {
        "type": "rect",
        "x0": core_x0,
        "x1": core_x1,
        "y0": 0,
        "y1": 1,
        "yref": "paper",
        "fillcolor": "rgba(255, 0, 0, 0.1)",
        "line": {"width": 0},
        "label": {"text": "Core Size", "textposition": "top center", "padding": 10},
        "fillcolor": color["core_bg"],
        "layer": "below",
    }

    fig.add_shape(highlight_shape)

    client = "Adidas"
    brands = list(set(df["brand"]))
    brands.remove(client)
    brands.insert(0, client)
    for brand in brands:
        brand_df = df[df["brand"] == brand]
        fig.add_trace(
            go.Bar(
                y=brand_df["brand"],
                base=brand_df["min"],
                x=brand_df["max"] - brand_df["min"],
                width=0.8,
                orientation="h",
                name=brand,
                hovertemplate="(%{base},%{x})",
                marker=dict(
                    color=color["client"] if brand == client else color["competitor"]
                ),
                text=df["name"],
                textposition="inside",
                texttemplate="%{text}  ",
                offset=-0.4,
            )
        )

    # single num
    clt_single_df = df[(df["min"] == df["max"]) & (df["brand"] == client)]
    cpt_single_df = df[(df["min"] == df["max"]) & (df["brand"] != client)]
    if not clt_single_df.empty:
        add_single_trace(fig, clt_single_df, True)
    if not cpt_single_df.empty:
        add_single_trace(fig, cpt_single_df, False)

    fig.update_yaxes(autorange="reversed", dtick=0.1)
    fig.update_layout(
        width=1000,
        title=dict(
            text="ttttt",
            pad=dict(l=300)
        ),
        plot_bgcolor="#FFFFFF",
        showlegend=False,
        xaxis=dict(
            title=dict(text="xtitle", font=dict(size=23)),
            tick0=int(min(df["min"]) / 2) * 2,  # set first tick
            dtick=2,  # set step
            tickfont=dict(size=16),
            gridcolor="#EFEFEF",
            griddash="dot",
            gridwidth=2,
            # linecolor="#B4C5D2",
            linewidth=0,
            layer="below traces"
            # range=(50, 110),
        ),
        yaxis=dict(
            tickfont=dict(size=16),
            # gridcolor="#EFEFEF",
        ),
    )
    fig.show()


def test_line():
    x = [58.00,58.50,59.00,59.50,60.00,60.50,61.00,61.50,62.00,62.50,63.00,63.50,64.00,64.50,65.00,65.50,66.00,66.50,67.00,67.50,68.00,68.50,69.00,69.50,70.00,70.50,71.00,71.50,72.00,72.50,73.00]
    y0 = [0.15,0.46,0.67,0.92,2.05,2.19,2.30,3.81,4.58,4.26,4.90,6.64,7.59,6.00,8.69,6.33,7.27,5.60,5.28,3.91,3.81,3.30,2.04,1.77,1.44,1.11,0.87,0.59,0.48,0.54,0.47]
    y1 = [1.15,1.46,1.67,1.92,3.05,3.19,3.3,4.81,5.58,5.26,5.9,7.64,8.59,7.0,9.69,7.33,8.27,6.6,6.28,4.91,4.81,4.3,3.04,2.77,2.44,2.11,1.87,1.59,1.48,1.54,1.47]
    datas = []
    for idx, v in enumerate(x):
        datas.append(dict(group="group1", size=v, pct=y0[idx]))
        datas.append(dict(group="group2", size=v, pct=y1[idx]))

    df = pd.DataFrame(datas)
    # fig = go.Figure(data=go.Scatter())

    # fig = px.line(df, x="size", y="pct", color='group', line_shape='spline')
    fig = go.Figure()
    df1 = df[df["group"] == "group1"]
    df2 = df[df["group"] == "group2"]

    # showlegend：是否展示对应的legend  visible: 是否展示对应的trace
    # fig.add_trace(go.Scatter(x=df1["size"], y=df1["pct"], line_shape='spline', line_smoothing=1.3, showlegend=False))
    # fig.add_trace(go.Scatter(x=df1["size"], y=df1["pct"], line_shape='spline', line_smoothing=1.3))
    # fig.add_trace(go.Scatter(x=df2["size"], y=df2["pct"], line_shape='spline', line_smoothing=0.5, visible=False))
    # fig.add_trace(go.Scatter(x=df2["size"], y=df2["pct"], line_shape='spline', line_smoothing=0.5))
    fill = 'none'
    # fill = 'tozeroy'
    # fill = 'tozerox'
    # fill = 'tonexty'
    # fill = 'tonextx'
    # fill = 'toself'
    trace0 = go.Scatter(x=df1["size"], y=df1["pct"], line_shape='spline', line_smoothing=1.3, name="group", fill=fill)
    trace1 = go.Scatter(x=df2["size"], y=df2["pct"], line_shape='spline', line_smoothing=0.5, name="group", fill=fill)
    fig.add_trace(trace0)
    fig.add_trace(trace1)

    # fig.update_traces(selector=dict(name="group1"), visible=False)

    fig.update_layout(
        width=1000,
        title=dict(
            text="ttttt",
            pad=dict(l=300)
        ),
        plot_bgcolor="#FFFFFF",
        showlegend=True,
        xaxis=dict(
            title=dict(text="xtitle", font=dict(size=23)),
            tick0=int(min(df["size"]) / 2) * 2,  # set first tick
            dtick=2,  # set step
            tickfont=dict(size=16),
            gridcolor="#EFEFEF",
            griddash="dot",
            gridwidth=2,
        ),
        yaxis=dict(
            title="",
            tickfont=dict(size=16),
            gridcolor="#EFEFEF",
            griddash="dot",
            gridwidth=2,
        )
    )
    fig.show()
    t1 = time.time()
    fig.write_image("./test.png", format="png")
    t2 = time.time()
    print(t2-t1)
    # go.Figure(**fig.to_dict()).show()

def test_sub():
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import pandas as pd
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/sales_success.csv')
    print(df.head())

    levels = ['salesperson', 'county', 'region']  # levels used for the hierarchical chart
    color_columns = ['sales', 'calls']
    value_column = 'calls'

    def build_hierarchical_dataframe(df, levels, value_column, color_columns=None):
        """
        Build a hierarchy of levels for Sunburst or Treemap charts.

        Levels are given starting from the bottom to the top of the hierarchy,
        ie the last level corresponds to the root.
        """
        df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        for i, level in enumerate(levels):
            df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
            dfg = df.groupby(levels[i:]).sum()
            dfg = dfg.reset_index()
            df_tree['id'] = dfg[level].copy()
            if i < len(levels) - 1:
                df_tree['parent'] = dfg[levels[i + 1]].copy()
            else:
                df_tree['parent'] = 'total'
            df_tree['value'] = dfg[value_column]
            df_tree['color'] = dfg[color_columns[0]] / dfg[color_columns[1]]
            df_all_trees = df_all_trees.append(df_tree, ignore_index=True)
        total = pd.Series(dict(id='total', parent='',
                               value=df[value_column].sum(),
                               color=df[color_columns[0]].sum() / df[color_columns[1]].sum()))
        df_all_trees = df_all_trees.append(total, ignore_index=True)
        return df_all_trees

    df_all_trees = build_hierarchical_dataframe(df, levels, value_column, color_columns)
    average_score = df['sales'].sum() / df['calls'].sum()

    # fig = make_subplots(1, 2, specs=[[{"type": "domain"}, {"type": "domain"}]], )
    fig = make_subplots(1, 1, specs=[[{"type": "domain"}]], )

    # fig.add_trace(go.Sunburst(
    #     labels=df_all_trees['id'],
    #     parents=df_all_trees['parent'],
    #     values=df_all_trees['value'],
    #     branchvalues='total',
    #     marker=dict(
    #         colors=df_all_trees['color'],
    #         colorscale='RdBu',
    #         cmid=average_score),
    #     hovertemplate='<b>%{label} </b> <br> Sales: %{value}<br> Success rate: %{color:.2f}',
    #     name=''
    # ), 1, 1)

    fig.add_trace(go.Sunburst(
        labels=df_all_trees['id'],
        parents=df_all_trees['parent'],
        values=df_all_trees['value'],
        branchvalues='total',
        marker=dict(
            colors=df_all_trees['color'],
            colorscale='RdBu',
            cmid=average_score),
        hovertemplate='<b>%{label} </b> <br> Sales: %{value}<br> Success rate: %{color:.2f}',
        maxdepth=2
    ))

    fig.update_layout(margin=dict(t=10, b=10, r=10, l=10))
    fig.show()


def load_json():
    import json
    import plotly.graph_objects as go
    with open("./fig.json", "r") as f:
        fig_json = json.load(f)

    # 使用 JSON 数据来创建一个新的图形
    new_fig = go.Figure(fig_json)

    # 显示新的图形
    # new_fig.show()
    print("start")
    new_fig.to_image(format="png")
    print("end")


if __name__ == "__main__":
    # test scatter plots
    # tp = TestPlotly()
    # tp.test_scatter_plots()

    # test timeline
    # test_timeline()

    # customer_bar()

    # test_line()

    # test_sub()
    load_json()






