from django.urls import path
from . import views

app_name = 'totolyzer'

urlpatterns = [
    path('simple-freq', views.simple_freq_view, name='chart-simple_freq'),
    path('best-pairs', views.simple_freq_view, name='chart-best_pairs'),
    path('day-of-week', views.simple_freq_view, name='chart-day_of_week'),
]
