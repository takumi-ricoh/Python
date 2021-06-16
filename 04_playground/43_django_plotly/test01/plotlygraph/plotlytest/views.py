from django.shortcuts import render, redirect
from .plotgraph import plotlytest_graph

def plotlytestviews(request):
    plot = plotlytest_graph()

    return render(request, 'plotlytest.html', {'plot': plot})
