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

# will need to create some custom permission classes to handle the
# many-to-many relationship between resident and carepartner
# If carepartner, then use user to lookup relationships and see if resident is in the list
# https://stackoverflow.com/questions/58224089/django-rest-framework-custom-permission-class-with-manytomanyfield
# If resident, simply look at the resident field of the table you are querying
# If researcher, allow all
# if admin, allow all

