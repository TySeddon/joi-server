"""
This module contains the serializers for the model.
This provides the translation between domain models (REST API) and data model (SQL database)
"""

from django.contrib.auth.models import User, Group
from rest_framework import serializers
import joi.models as models

# https://docs.djangoproject.com/en/2.2/topics/serialization/
# https://www.django-rest-framework.org/api-guide/serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resident
        fields = '__all__'

class CarePartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarePartner
        fields = '__all__'

class CarePartnerResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarePartnerResident
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device
        fields = '__all__'

class MemoryBoxTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MemoryBoxType
        fields = '__all__'

class MemoryBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MemoryBox
        fields = '__all__'

class MemmoryBoxSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MemmoryBoxSession
        fields = '__all__'

class MemoryBoxSessionMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MemoryBoxSessionMedia
        fields = '__all__'

class MediaInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MediaInteraction
        fields = '__all__'

