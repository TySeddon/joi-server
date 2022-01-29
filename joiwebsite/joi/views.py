import logging
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Permission, User, Group
from rest_framework import exceptions, viewsets, permissions, status, generics
from rest_framework.response import Response
import joi.models as models
import joi.serializers as serializers
from joi.permissions import IsOwnerOrAdmin, IsAdminOrReadOnly, IsCarePartnerOfResident


def index(request):
    context = {}
    return render(request, 'joi/home.html', context)    

def spotify(request):
    context = {}
    return render(request, 'joi/spotify.html', context)        

class ResidentAuthorizedViewSet(viewsets.ModelViewSet):
    """
    Base class for objects that are associated with a Resident
    and should only be viewable and editable by associated CarePartners or Admin
    """
    permission_classes = [permissions.IsAuthenticated, IsCarePartnerOfResident]
    #filterset_fields = ['resident']

    def list(self, request, *args, **kwargs):
        if not bool(request.user and request.user.is_authenticated):
            raise exceptions.NotAuthenticated()
        queryset = None
        if request.user.is_staff:                
            # if Admin, then show all data
            queryset = self.get_queryset()
        else:
            # get CarePartner object for current user
            user_carepartner = models.CarePartner.objects.filter(user=request.user).first()
            if user_carepartner is not None:
                # get list of Residents associated with this CarePartner
                residents = models.CarePartnerResident.objects.filter(carepartner=user_carepartner).values_list('resident_id', flat=True)
                # filter list to those Residents
                queryset = self.get_queryset().filter(resident_id__in=residents)
            else:
                queryset = None                
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)   

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users to be viewed or edited.
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
    API endpoint that allows Groups to be viewed or edited.
    Only admins can view and edit groups.
    """
    permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]    
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer

class ResidentViewSet(ResidentAuthorizedViewSet):
    """
    API endpoint that allows Residents to be viewed or edited.
    Admins and Researchers can view and edit Residents
    CarePartners can only view their Residents
    Residents can only view themselves
    """
    queryset = models.Resident.objects.all()
    serializer_class = serializers.ResidentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCarePartnerOfResident]

# will need to create some custom permission classes to handle the
# many-to-many relationship between resident and carepartner
# If carepartner, then use user to lookup relationships and see if resident is in the list
# https://stackoverflow.com/questions/58224089/django-rest-framework-custom-permission-class-with-manytomanyfield
# If resident, simply look at the resident field of the table you are querying
# If researcher, allow all
# if admin, allow all

class MemoryBoxTypeViewSet(viewsets.ModelViewSet):
    queryset = models.MemoryBoxType.objects.all()
    serializer_class = serializers.MemoryBoxTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

class CarePartnerResidentViewSet(ResidentAuthorizedViewSet):
    """
    API endpoint that allows Residents to be viewed or edited.
    Admins and Researchers can view and edit Residents
    CarePartners can only view their Residents
    Residents can only view themselves
    """
    queryset = models.CarePartnerResident.objects.all()
    serializer_class = serializers.CarePartnerResidentSerializer
