from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.urls import path

def home_view(request):
    return redirect('portfolio:index')

def my_custom_page_not_found_view(request,exception):
    return render(request,'404.html',status=404)

def site_ownership_verification(request):
    return render(request,'googlee3d9d4182d6536a0.html')