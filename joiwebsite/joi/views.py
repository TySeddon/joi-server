import logging
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Permission, User, Group
from rest_framework import exceptions, viewsets, permissions, status, generics
from rest_framework.response import Response
import joiwebsite.joi.models as models
import joiwebsite.joi.serializers as serializers
from joiwebsite.joi.permissions import IsOwnerOrAdmin, IsAdminOrReadOnly


def index(request):
    context = {}
    return render(request, 'joi/home.html', context)    

def spotify(request):
    context = {}
    return render(request, 'joi/spotify.html', context)        

class ResidentViewSet(viewsets.ModelViewSet):
    queryset = models.Resident.objects.all()
    serializer_class = serializers.ResidentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

