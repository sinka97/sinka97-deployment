from django.urls import path
from .views import overview,simple_freq,hot_n_cold,best_pairs,daily_breakdown,monthly_breakdown

app_name = 'totolyzer'

urlpatterns = [
    path('', overview.overview_view, name='chart-overview'),
    path('overview', overview.overview_view, name='chart-overview'),
    path('simple-freq', simple_freq.simple_freq_view, name='chart-simple_freq'),
    path('hot-n-cold', hot_n_cold.hot_n_cold_view, name='chart-hot_n_cold'),
    path('best-pairs', best_pairs.best_pairs_view, name='chart-best_pairs'),
    path('daily-breakdown', daily_breakdown.daily_breakdown_view, name='chart-daily_breakdown'),
    path('monthly-breakdown', monthly_breakdown.monthly_breakdown_view, name='chart-monthly_breakdown'),
]
