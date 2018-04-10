# -*- coding: utf-8 -*-
"""
Spyderエディタ

これは一時的なスクリプトファイルです
"""

from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show, reset_output
from bokeh.models import HoverTool
import csv
import numpy as np

#データ読み出し
csvdata=[]
with open("testdata.csv","r") as f:
    reader = csv.reader(f)
    for row in reader:
        csvdata.append(row)
csvdata=np.array(csvdata)

#output_fileのサイズが増えないよう、おまじない
reset_output()

#データの生成
x = np.float32(csvdata[:,0])
y1 = np.float32(csvdata[:,1])
y2 = np.float32(csvdata[:,2])
output_file("定着温度グラフ.html")

#hoverの設定
hover = HoverTool(
    tooltips=[("index", "$index"),("(x,y)", "($x, $y)"),],
    mode = "mouse")
tools=["pan", "wheel_zoom", "box_zoom", "xbox_zoom",hover,"undo","reset"]

#figreオブジェクトの作成
p = figure(title="line",x_axis_label="時刻[sec]",y_axis_label="温度[℃]",plot_width=1000,tools=tools,)
p.xaxis.axis_label_text_font_size = "20pt"
p.yaxis.axis_label_text_font_size = "20pt"

#背景の設定
p.background_fill_color = "beige"

#プロットの追加
p.line(x,y1,legend="Temp1",line_width=2,line_color="red")
p.circle(x,y1,legend="Temp1",size=4,color="red")
p.line(x,y2,legend="Temp2",line_width=2,line_color="blue")
p.circle(x,y2,legend="Temp2",size=4,color="blue",)

p.legend.click_policy="hide"

show(p)

a=curdoc()