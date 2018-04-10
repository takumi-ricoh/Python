# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 12:45:50 2018

@author: p000495138
"""

import numpy as np
import time

from bokeh.io import curdoc
import bokeh.plotting as plotting
from bokeh.models import GlyphRenderer

#動かない

class LiveMonitor(object):

    def __init__(self, server='chainer', url='http://localhost:5002/', **kwargs):
        # 出力先に IPython Notebook を指定
        #plotting.output_notebook()
        plotting.output_file("test.html")
        
        # figure を定義
        self.fig = self._initialize_figure()
                                                  
        # グリッドを描画
        plotting.show(self.fig)

    def _initialize_figure(self):
        """ figure の初期化用のメソッド"""

        figure = plotting.figure()

        # 空のデータで折れ線グラフを作成
        x = np.array([])
        y = np.array([])
        figure.line(x, y)
        return figure

    def update(self, value=None):
        """
        プロットを更新するためのメソッド
        指定したキーワード引数に対応する figure が更新される
        """
        self._maybe_update(self.fig,  value)

    def _maybe_update(self, figure, value):
        """ figure の値を更新するメソッド"""

        # figure が利用している data_source を取得
        renderer = figure.select(dict(type=GlyphRenderer))
        ds = renderer[0].data_source

        # data_source 中の値を更新
        y = np.append(ds.data['y'], value)
        ds.data['y'] = y
        ds.data['x'] = np.arange(len(y))

        # session へ返す (とプロットが更新される)
        #plotting.curdoc()
        #plotting.cursession().store_objects(ds)
        
monitor = LiveMonitor()

curdoc().add_root(monitor.fig)
curdoc().add_periodic_callback(monitor.update, 30)

#for i in range(100):
#    x = np.linspace(0,10,100)
#    y = np.sin(x)
#    monitor.update(y)
#    time.sleep(1)
    
