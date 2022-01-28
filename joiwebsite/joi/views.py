import logging
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Permission, User, Group
from rest_framework import exceptions, viewsets, permissions, status, generics
from rest_framework.response import Response
import joi.models as models
import joi.serializers as serializers
from joi.permissions import IsOwnerOrAdmin, IsAdminOrReadOnly


def index(request):
    context = {}
    return render(request, 'joi/home.html', context)    

def spotify(request):
    context = {}
    return render(request, 'joi/spotify.html', context)        

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    Anyone can POST to create a new user.  All other operations require authentication and authorization.
    Users can only view their user account.  Admins can see all users.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = [IsOwnerOrAdmin]
    http_method_names = ['get', 'head']

    def list(self, request, *args, **kwargs):
        if not bool(request.user and request.user.is_authenticated):
            raise exceptions.NotAuthenticated()
        queryset = None
        userid = self.request.query_params.get('user')
        if userid is not None:
            if int(userid) == request.user.id or request.user.is_staff:
                queryset = self.get_queryset().filter(id=userid)
        elif request.user.is_staff:                
            queryset = self.get_queryset()
        else:
            queryset = self.get_queryset().filter(id=request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)    

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    Only admins can view and edit groups.
    """
    permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]    
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    
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

