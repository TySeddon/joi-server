import uuid
import datetime
import pytz
#from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
import joi.models as models

UUID_0 = uuid.UUID("00000000-0000-0000-0000-000000000000")
UUID_1 = uuid.UUID("00000000-0000-0000-0000-000000000001")
UUID_2 = uuid.UUID("00000000-0000-0000-0000-000000000002")
UUID_3 = uuid.UUID("00000000-0000-0000-0000-000000000003")
UUID_4 = uuid.UUID("00000000-0000-0000-0000-000000000004")
UUID_5 = uuid.UUID("00000000-0000-0000-0000-000000000005")

# def get_uuid(prefix):
#     if prefix == "test_":
#         return uuid.UUID("00000000-0000-0000-0000-000000000001")
#     elif prefix == "demo_":
#         return uuid.UUID("00000000-0000-0000-0000-000000000002")
#     elif prefix == "unittest_":
#         return uuid.UUID("00000000-0000-0000-0000-000000000003")

def delete_data():
    User.objects.delete()

def initialize_data():
    create_users()

def create_users():
    User.objects.all().delete()

    # create CarePartner Users
    User.objects.create_user(
        username="cp_1", email='cp_1@cognivista.com', password='testpassword').save()
    User.objects.create_user(
        username="cp_2", email='cp_2@cognivista.com', password='testpassword').save()

def create_residents():
    models.Resident.objects.all().delete()

    models.Sensor.objects.bulk_create(
        [
            models.Resident(
                resident_id=UUID_1,
                first_name="Ruth",
                last_name="Resident",
                is_active = True
            ),
            models.Resident(
                resident_id=UUID_2,
                first_name="Bob",
                last_name="Resident",
                is_active = True
            )
        ]
    )

def create_carepartners():
    models.CarePartner.objects.all().delete()

    user_carepartner_1 = User.objects.filter(username="cp_1").first()
    user_carepartner_2 = User.objects.filter(username="cp_2").first()

    models.CarePartner.objects.bulk_create(
        [
            models.CarePartner(
                carepartner_id=UUID_1,
                user=user_carepartner_1,
                first_name="Lisa",
                last_name="CarePartner",
                is_active = True
            ),
            models.CarePartner(
                carepartner_id=UUID_2,
                user=user_carepartner_2,
                first_name="Thomas",
                last_name="CarePartner",
                is_active = True
            )
        ]
    )

def create_carepartnerresidents():
    models.CarePartnerResident.objects.all().delete()

    resident_1 = models.Resident.objects.filter(pk=UUID_1).first()
    resident_2 = models.Resident.objects.filter(pk=UUID_2).first()
    carepartner_1 = models.CarePartner.objects.filter(pk=UUID_1).first()
    carepartner_2 = models.CarePartner.objects.filter(pk=UUID_2).first()

    models.CarePartnerResident.objects.bulk_create(
        [
            models.CarePartnerResident(
                carepartner_resident_id=UUID_1,
                carepartner=carepartner_1,
                resident=resident_1
            ),
            models.CarePartnerResident(
                carepartner_resident_id=UUID_2,
                carepartner=carepartner_2,
                resident=resident_2
            )
        ]
    )
