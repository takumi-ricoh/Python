from django.urls import path
from .views import plotlytestviews

urlpatterns = [
    path('plotlytest/', plotlytestviews, name='plotlytest'),
 ]
