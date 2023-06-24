from django.urls import path
from .views import simple_freq,hot_n_cold,best_pairs

app_name = 'totolyzer'

urlpatterns = [
    path('simple-freq', simple_freq.simple_freq_view, name='chart-simple_freq'),
    path('hot-n-cold', hot_n_cold.hot_n_cold_view, name='chart-hot_n_cold'),
    path('best-pairs', best_pairs.best_pairs_view, name='chart-best_pairs'),
]
