from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'joi/home.html', context)    

def music(request):
    context = {}
    return render(request, 'joi/music.html', context)    