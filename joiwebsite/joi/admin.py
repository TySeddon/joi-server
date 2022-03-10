import uuid
from django.contrib import admin
import joi.models as models


@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'name', 'description', 'resident']

    def get_changeform_initial_data(self, request):
        return {'device_id': uuid.uuid4()}

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('device_id',)
        return self.readonly_fields        

@admin.register(models.Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ['resident_id', 'first_name', 'last_name']

    def get_changeform_initial_data(self, request):
        return {'resident_id': uuid.uuid4()}

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('resident_id',)
        return self.readonly_fields        

@admin.register(models.CarePartner)
class CarePartnerAdmin(admin.ModelAdmin):
    list_display = ['carepartner_id', 'first_name', 'last_name']

    def get_changeform_initial_data(self, request):
        return {'carepartner_id': uuid.uuid4()}

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('carepartner_id',)
        return self.readonly_fields        

@admin.register(models.CarePartnerResident)
class CarePartnerResidentAdmin(admin.ModelAdmin):
    list_display = ['carepartner', 'resident']

    def get_changeform_initial_data(self, request):
        return {'carepartner_resident_id': uuid.uuid4()}

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('carepartner_resident_id',)
        return self.readonly_fields        

@admin.register(models.MemoryBox)
class MemoryBoxAdmin(admin.ModelAdmin):
    list_display = ['memorybox_type', 'resident', 'name', 'description']

    def get_changeform_initial_data(self, request):
        return {'memorybox_id': uuid.uuid4()}

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('memorybox_id',)
        return self.readonly_fields        

admin.site.register(models.MemoryBoxSession)
admin.site.register(models.MemoryBoxSessionMedia)
admin.site.register(models.MediaInteraction)
