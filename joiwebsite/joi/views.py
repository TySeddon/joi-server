from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'joi/home.html', context)    

def youtubemusic(request):
    context = {}
    return render(request, 'joi/youtubemusic.html', context)    

def spotify(request):
    context = {}
    return render(request, 'joi/spotify.html', context)        

def spotifycontroller(request):
    context = {}
    return render(request, 'joi/spotifycontroller.html', context)        
