from django.shortcuts import render
from django.http.response import HttpResponse,Http404,HttpResponseRedirect
from django.urls import reverse

# Create your views here.


def index_view(request):
    return render(request,'portfolio/index.html')

def about_me_view(request):
    return render(request,'portfolio/about-me.html')

def portfolio_view(request):
    return render(request,'portfolio/my-portfolio.html')
