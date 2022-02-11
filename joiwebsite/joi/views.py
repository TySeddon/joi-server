import logging
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Permission, User, Group
from rest_framework import exceptions, viewsets, permissions, status, generics
from rest_framework.response import Response
import joi.models as models
import joi.serializers as serializers
from joi.permissions import IsOwnerOrAdmin, IsAdminOrReadOnly, IsCarePartnerOfResident, is_member

def index(request):
    context = {}
    return render(request, 'joi/home.html', context)    

def spotify(request):
    context = {}
    return render(request, 'joi/spotify.html', context)        

def slideshow(request):
    context = {}
    return render(request, 'joi/slideshow.html', context)        

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
        if request.user.is_staff or is_member(request.user,'Researcher'):          
            # if Admin or Researcher, then show all data
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
        if request.user.is_staff:                
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

class CarePartnerResidentViewSet(ResidentAuthorizedViewSet):
    """
    API endpoint that allows Residents to be viewed or edited.
    Admins and Researchers can view and edit Residents
    CarePartners can only view their Residents
    Residents can only view themselves
    """
    queryset = models.CarePartnerResident.objects.all()
    serializer_class = serializers.CarePartnerResidentSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Devices to be viewed or edited.
    All Devices are public readonly.  Admins can edit them.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAdminOrReadOnly]    
    queryset = models.Device.objects.all()
    serializer_class = serializers.DeviceSerializer

class MemoryBoxTypeViewSet(viewsets.ModelViewSet):
    queryset = models.MemoryBoxType.objects.all()
    serializer_class = serializers.MemoryBoxTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

class MemoryBoxViewSet(ResidentAuthorizedViewSet):
    """
    API endpoint that allows MemoryBox to be viewed or edited.
    Admins and Researchers can view and edit all MemoryBoxes
    CarePartners can only edit their Residents' MemoryBoxes
    Residents can only view and edit their MemoryBoxes
    """
    queryset = models.MemoryBox.objects.all()
    serializer_class = serializers.MemoryBoxSerializer    

class MemoryBoxSessionViewSet(ResidentAuthorizedViewSet):
    """
    API endpoint that allows MemoryBoxSessions to be viewed or edited.
    Admins and Researchers can view and edit all MemoryBoxSessions
    CarePartners can only edit their Residents' MemoryBoxSessions
    Residents can only view and edit their MemoryBoxSessions
    """
    queryset = models.MemoryBoxSession.objects.all()
    serializer_class = serializers.MemoryBoxSessionSerializer      

class MemoryBoxSessionMediaViewSet(ResidentAuthorizedViewSet):
    """
    """
    queryset = models.MemoryBoxSessionMedia.objects.all()
    serializer_class = serializers.MemoryBoxSessionMediaSerializer          

class MediaInteractionViewSet(ResidentAuthorizedViewSet):
    """
    """
    queryset = models.MediaInteraction.objects.all()
    serializer_class = serializers.MediaInteractionSerializer              

class SlideshowViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = models.Slideshow.objects.all()
    serializer_class = serializers.SlideshowSerializer                  
    permission_classes = [permissions.AllowAny]  # todo: lock this down later

