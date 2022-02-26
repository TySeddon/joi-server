import logging
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Permission, User, Group
from rest_framework import exceptions, viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
import joi.models as models
import joi.serializers as serializers
from joi.permissions import IsOwnerOrAdmin, IsAdminOrReadOnly, IsCarePartnerOfResident, is_member

def index(request):
    context = {}
    return render(request, 'joi/home.html', context)    

def joi_home(request):
    context = {}
    return render(request, 'joi/joi_home.html', context)    

def spotify(request):
    context = {}
    return render(request, 'joi/spotify.html', context)        

def slideshow(request):
    context = {}
    return render(request, 'joi/slideshow.html', context)        

def memorybox_sessions_list(request):
    memorybox_sessions = models.MemoryBoxSession.objects.all()
    context = {
        'memorybox_sessions':memorybox_sessions
    }
    return render(request, 'joi/reports/memorybox_sessions_list.html', context)        

def memorybox_session_report(request):
    memorybox_session_id = request.GET.get('id', '735d7a1c-fb8c-4831-ba6c-67c6c0eb4c7d')
    memorybox_session = models.MemoryBoxSession.objects.filter(memorybox_session_id=memorybox_session_id).first()
    context = {
        'memorybox_session':memorybox_session
    }
    return render(request, 'joi/reports/memorybox_session_report.html', context)        

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

        device_id = self.request.query_params.get('device')        
        if request.user.is_staff or is_member(request.user,'Researcher'):          
            # if Admin or Researcher, then show all data
            if device_id:
                queryset = self.get_queryset().filter(device_id=device_id)
            else:
                queryset = self.get_queryset()
        else:
            # see if user is resident
            resident = models.Resident.objects.filter(user=request.user).first()
            if resident is not None:
                if device_id:
                    queryset = self.get_queryset().filter(resident_id=resident.resident_id, device_id=device_id)
                else:                    
                    queryset = self.get_queryset().filter(resident_id=resident.resident_id)
            else:
                # see if user is care partner
                user_carepartner = models.CarePartner.objects.filter(user=request.user).first()
                if user_carepartner is not None:
                    # get list of Residents associated with this CarePartner
                    residents = models.CarePartnerResident.objects.filter(carepartner=user_carepartner).values_list('resident_id', flat=True)
                    # filter list to those Residents
                    if device_id:
                        queryset = self.get_queryset().filter(resident_id__in=residents, device_id=device_id)
                    else:                        
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


    serializer_action_classes = {
        'end': serializers.EndMemoryBoxSessionSerializer,
    }    

    def get_serializer_class(self):
        try:
            print(self.action)
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MemoryBoxSessionViewSet, self).get_serializer_class()    

    @action(detail=True, methods=['post'])
    def end(self, request, pk=None, version=None):
        obj = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():           
            obj.session_end_method = serializer.data.get("session_end_method")
            obj.session_end_datetime = serializer.data.get("session_end_datetime")
            obj.resident_self_reported_feeling = serializer.data.get("resident_self_reported_feeling")
            obj.save()
            return Response({'detail': 'record updated'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemoryBoxSessionMediaViewSet(ResidentAuthorizedViewSet):
    """
    """
    queryset = models.MemoryBoxSessionMedia.objects.all()
    serializer_class = serializers.MemoryBoxSessionMediaSerializer  

    serializer_action_classes = {
        'end': serializers.EndMemoryBoxSessionMediaSerializer,
    }    

    def get_serializer_class(self):
        try:
            print(self.action)
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MemoryBoxSessionMediaViewSet, self).get_serializer_class()    

    @action(detail=True, methods=['post'])
    def end(self, request, pk=None, version=None):
        obj = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():           
            obj.media_end_datetime = serializer.data.get("media_end_datetime")
            obj.media_percent_completed = serializer.data.get("media_percent_completed")
            obj.resident_motion = serializer.data.get("resident_motion")
            obj.resident_utterances = serializer.data.get("resident_utterances")
            obj.resident_self_reported_feeling = serializer.data.get("resident_self_reported_feeling")
            obj.save()
            return Response({'detail': 'record updated'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MediaInteractionViewSet(ResidentAuthorizedViewSet):
    """
    """
    queryset = models.MediaInteraction.objects.all()
    serializer_class = serializers.MediaInteractionSerializer              

class DeviceMessageViewSet(ResidentAuthorizedViewSet):
    """
    """
    queryset = models.DeviceMessage.objects.all()
    serializer_class = serializers.DeviceMessageSerializer              

class SlideshowViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = models.Slideshow.objects.all()
    serializer_class = serializers.SlideshowSerializer                  
    permission_classes = [permissions.AllowAny]  # todo: lock this down later

