from django.contrib import admin

# Register your models here.

import joi.models as models

@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'name', 'description', 'resident']

@admin.register(models.Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ['resident_id', 'first_name', 'last_name']

@admin.register(models.CarePartner)
class CarePartnerAdmin(admin.ModelAdmin):
    list_display = ['carepartner_id', 'first_name', 'last_name']

@admin.register(models.CarePartnerResident)
class CarePartnerResidentAdmin(admin.ModelAdmin):
    list_display = ['carepartner', 'resident']

@admin.register(models.MemoryBox)
class MemoryBoxAdmin(admin.ModelAdmin):
    list_display = ['memorybox_type', 'resident', 'name', 'description']

admin.site.register(models.MemoryBoxSession)
admin.site.register(models.MemoryBoxSessionMedia)
admin.site.register(models.MediaInteraction)
