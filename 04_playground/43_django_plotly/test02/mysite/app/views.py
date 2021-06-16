from django.shortcuts import render

# Create your views here.
"""
ビューを作成します。ここが今回のポイントです。plotly.pyで描画したデータをHTMLに出力してテンプレートに渡します。今回は TemplateView を利用します(❶)。

plotly.pyには figure と呼ばれる描画領域を管理するオブジェクトがあり、このオブジェクトからHTML上にグラフを描画したり、Jupyter上にグラフを描画できます。今回は紹介していませんが、 Plotly Express についても同様です。

度々の宣伝ですが、plotly.py(Plotly Express)ついても共著 Python インタラクティブ・データビジュアライゼーション入門 ―Plotly/Dashによるデータ可視化とWebアプリ構築― にて詳しく解説しています。

figure オブジェクトをHTMLに出力するには to_html メソッドを実行します(❷)。plotly.pyは plotly.js が元になったラッパーで、HTMLにはJavaScriptが含まれますが、後述するCDNを利用するため、引数 include_plotlyjs を False にしてJavaScript部分以外を出力します。

plotly.pyのグラフがHTML化できたので、これを TemplateView に追加します(❸)。
"""

from django.views.generic import TemplateView  # ❶
import plotly.graph_objects as go


def line_charts():
    fig = go.Figure(
        go.Scatter(x=[1, 2, 3], y=[3, 5, 2]), layout=go.Layout(width=400, height=400)
    )
    return fig.to_html(include_plotlyjs=False)  # ❷


class LineChartsView(TemplateView):  # ❶
    template_name = "plot.html"

    def get_context_data(self, **kwargs):
        context = super(LineChartsView, self).get_context_data(**kwargs)
        context["plot"] = line_charts()  # ❸
        return context