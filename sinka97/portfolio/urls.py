from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('',views.index_view),
    path('home/',views.index_view,name='index'),
    path('about-me/',views.about_me_view,name='about-me'),
    path('my-portfolio/',views.portfolio_view,name='my-portfolio'),
]