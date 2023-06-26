from django.urls import path
from .views import overview,simple_freq,hot_n_cold,best_pairs,mean_analysis

app_name = 'totolyzer'

urlpatterns = [
    path('', overview.overview_view, name='chart-overview'),
    path('overview', overview.overview_view, name='chart-overview'),
    path('simple-freq', simple_freq.simple_freq_view, name='chart-simple_freq'),
    path('hot-n-cold', hot_n_cold.hot_n_cold_view, name='chart-hot_n_cold'),
    path('best-pairs', best_pairs.best_pairs_view, name='chart-best_pairs'),
    path('mean-analysis', mean_analysis.mean_analysis_view, name='chart-mean_analysis'),
]
