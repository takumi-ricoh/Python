
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.offline import plot
import pandas as pd

def plotlytest_graph():
    df_positive = pd.read_csv('https://www.mhlw.go.jp/content/pcr_positive_daily.csv')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_positive['日付'], y=df_positive['PCR 検査陽性者数(単日)'],
                             mode='lines',
                             name='positive'))

    fig.layout.update({'title': 'positive'})
    fig.layout.xaxis.update({'title': 'date'})
    fig.layout.yaxis.update({'title': 'count'})
    fig.update_layout(title_text='Covid-19 Positive Plot(Japan Total)')
    plot_fig = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_fig