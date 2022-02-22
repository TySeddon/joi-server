import uuid
from django.utils import timezone
from datetime import datetime, timedelta
import pytz
#from django.contrib.gis.geos import Point
from django.contrib.auth.models import User, Group
import joi.models as models

UUID_0 = uuid.UUID("00000000-0000-0000-0000-000000000000")
UUID_1 = uuid.UUID("00000000-0000-0000-0000-000000000001")
UUID_2 = uuid.UUID("00000000-0000-0000-0000-000000000002")
UUID_3 = uuid.UUID("00000000-0000-0000-0000-000000000003")
UUID_4 = uuid.UUID("00000000-0000-0000-0000-000000000004")
UUID_5 = uuid.UUID("00000000-0000-0000-0000-000000000005")

MUSIC_TYPE = 1
PHOTO_TYPE = 2

# def get_uuid(prefix):
#     if prefix == "test_":
#         return uuid.UUID("00000000-0000-0000-0000-000000000001")
#     elif prefix == "demo_":
#         return uuid.UUID("00000000-0000-0000-0000-000000000002")
#     elif prefix == "unittest_":
#         return uuid.UUID("00000000-0000-0000-0000-000000000003")

def delete_data():
    models.MediaInteraction.objects.all().delete()
    models.MemoryBoxSessionMedia.objects.all().delete()
    models.MemoryBoxSession.objects.all().delete()
    models.MemoryBox.objects.all().delete()
    models.MemoryBoxType.objects.all().delete()
    models.Device.objects.all().delete()
    models.CarePartnerResident.objects.all().delete()
    models.CarePartner.objects.all().delete()
    models.Resident.objects.all().delete()
    User.objects.all().delete()
    Group.objects.all().delete()

def initialize_data():
    create_groups()
    create_users()
    create_residents()
    create_carepartners()
    create_carepartnerresidents()
    create_devices()
    create_memoryboxtypes()
    create_memoryboxes()
    create_memoryboxesessions()
    create_memoryboxesessionmedia()
    create_mediainteractions()

def create_groups():
    Group.objects.all().delete()

    Group.objects.bulk_create(
        [
            Group(name='Researcher')
        ]
    )


def create_users():
    User.objects.all().delete()

    # create admin user for testing
    User.objects.create_superuser(
        username="admin_1", email='admin_1@cognivista.com', password='testpassword').save()

    # create researcher for testing
    User.objects.create_user(
        username="researcher_1", email='researcher_1@cognivista.com', password='testpassword').save()
    # add researcher_1 to Research group
    researcher_1 = User.objects.get(username='researcher_1')
    researcher_group = Group.objects.get(name='Researcher')
    researcher_1.groups.add(researcher_group)

    # create Resident Users for testing
    User.objects.create_user(
        username="ruth", email='joi-ruth@cognivista.com', password='testpassword').save()
    User.objects.create_user(
        username="bob", email='joi-bob@cognivista.com', password='testpassword').save()

    # create CarePartner Users for testing
    User.objects.create_user(
        username="cp_1", email='cp_1@cognivista.com', password='testpassword').save()
    User.objects.create_user(
        username="cp_2", email='cp_2@cognivista.com', password='testpassword').save()

def create_residents():
    models.Resident.objects.all().delete()

    user_resident_1 = User.objects.filter(username="ruth").first()
    user_resident_2 = User.objects.filter(username="bob").first()

    models.Resident.objects.bulk_create(
        [
            models.Resident(
                resident_id=UUID_1,
                first_name="Ruth",
                last_name="Resident",
                user = user_resident_1,
                is_active = True,
                knowledge_base_name = "joi-ruth"
            ),
            models.Resident(
                resident_id=UUID_2,
                first_name="Bob",
                last_name="Resident",
                user = user_resident_2,
                is_active = True,
                knowledge_base_name = "joi-bob"
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

def create_devices():
    models.Device.objects.all().delete()

    resident_1 = models.Resident.objects.filter(pk=UUID_1).first()
    resident_2 = models.Resident.objects.filter(pk=UUID_2).first()

    models.Device.objects.bulk_create(
        [
            models.Device(
                device_id=UUID_1,
                name="Joi-Dev",
                description="Joi development environment",
                resident=resident_1,
                is_active = True
            ),
            models.Device(
                device_id=UUID_2,
                name="Joi-Test",
                description="Joi test environment",
                resident=resident_1,
                is_active = True
            ),
            models.Device(
                device_id=UUID_3,
                name="Joi-Demo",
                description="Joi demo environment",
                resident=resident_1,
                is_active = True
            ),
        ]
    )

def create_memoryboxtypes():
    models.MemoryBoxType.objects.all().delete()

    models.MemoryBoxType.objects.bulk_create(
        [
            models.MemoryBoxType(
                memorybox_type_id=MUSIC_TYPE,
                name="Music Memory Box",
                description="Spotify playlist"
            ),
            models.MemoryBoxType(
                memorybox_type_id=PHOTO_TYPE,
                name="Photo Memory Box",
                description="Google photo album"
            ),
        ]
    )    

def create_memoryboxes():
    models.MemoryBox.objects.all().delete()

    resident_1 = models.Resident.objects.filter(pk=UUID_1).first()
    resident_2 = models.Resident.objects.filter(pk=UUID_2).first()

    models.MemoryBox.objects.bulk_create(
        [
            models.MemoryBox(
                memorybox_id=UUID_1,
                memorybox_type_id=MUSIC_TYPE,
                resident=resident_1,
                name="1963 Music Memory Box",
                description="1963 Music",
                url="2LjLbyEEw9aRqMZo5qpK4O",
                is_active = True
            ),
            models.MemoryBox(
                memorybox_id=UUID_2,
                memorybox_type_id=PHOTO_TYPE,
                resident=resident_1,
                name="Photo Memory Box",
                description="Family and Flowers",
                url="ABsI1v6-zPvpuVn4RREb_3zlxSm2Q3sfQKI5Uhk2jImQZ7HdtXk9SZd5vKEAyML9sARGPuHaf8_i",
                is_active = True
            ),
        ]
    )    

def create_memoryboxesessions():
    models.MemoryBoxSession.objects.all().delete()

    resident_1 = models.Resident.objects.filter(pk=UUID_1).first()
    resident_2 = models.Resident.objects.filter(pk=UUID_2).first()

    models.MemoryBoxSession.objects.bulk_create(
        [
            models.MemoryBoxSession(
                memorybox_session_id=UUID_1,
                memorybox_id=UUID_1,
                resident=resident_1,
                device_id=UUID_1,
                session_start_method="user said: play music",
                session_end_method="natural",
                session_start_datetime=datetime.utcnow().replace(tzinfo=pytz.utc),
                session_end_datetime=(datetime.utcnow() + timedelta(seconds=30)).replace(tzinfo=pytz.utc),
            ),
            models.MemoryBoxSession(
                memorybox_session_id=UUID_2,
                memorybox_id=UUID_2,
                resident=resident_1,
                device_id=UUID_1,
                session_start_method="user said: play photos",
                session_end_method="natural",
                session_start_datetime=datetime.utcnow().replace(tzinfo=pytz.utc),
                session_end_datetime=(datetime.utcnow() + timedelta(seconds=30)).replace(tzinfo=pytz.utc),
            ),
        ]
    )    

def create_memoryboxesessionmedia():
    models.MemoryBoxSessionMedia.objects.all().delete()

    resident_1 = models.Resident.objects.filter(pk=UUID_1).first()
    resident_2 = models.Resident.objects.filter(pk=UUID_2).first()

    models.MemoryBoxSessionMedia.objects.bulk_create(
        [
            models.MemoryBoxSessionMedia(
                memorybox_session_media_id=UUID_1,
                memorybox_session_id=UUID_1,
                resident=resident_1,
                media_url="NA",
                media_start_datetime=datetime.utcnow().replace(tzinfo=pytz.utc),
                media_end_datetime=(datetime.utcnow() + timedelta(seconds=30)).replace(tzinfo=pytz.utc),
                media_percent_completed=1,
                media_name="test",
                media_artist="Elvis",
                media_tags="NA",
                media_classification="NA",
                media_features='{"id":"2EPr9Wx7e1cpGEbNAtuN7x","key":3,"uri":"spotify:track:2EPr9Wx7e1cpGEbNAtuN7x","mode":1,"type":"audio_features","tempo":160.753,"energy":0.805,"valence":0.969,"liveness":0.0938,"loudness":-7.436,"track_href":"https://api.spotify.com/v1/tracks/2EPr9Wx7e1cpGEbNAtuN7x","duration_ms":150160,"speechiness":0.0368,"acousticness":0.398,"analysis_url":"https://api.spotify.com/v1/audio-analysis/2EPr9Wx7e1cpGEbNAtuN7x","danceability":0.549,"time_signature":4,"instrumentalness":0.00000129}',
                resident_motion='{"history":[0,0,1,1,1,1,1,1,1,1,1],"percent":0.82,"end_time":"2022-02-21T17:13:26.426282","start_time":"2022-02-21T17:13:14.775940","num_of_seconds":11,"motion_event_pairs":[["2022-02-21T17:13:14.860799","2022-02-21T17:13:15.772985"],["2022-02-21T17:13:16.399637","2022-02-21T17:13:26.426186"]],"rolling_history_5sec":[0,0,0,0,0.6,0.8,1,1,1,1,1],"rolling_history_10sec":[0,0,0,0,0,0,0,0,0,0.8,0.9]}',
            ),
            models.MemoryBoxSessionMedia(
                memorybox_session_media_id=UUID_2,
                memorybox_session_id=UUID_1,
                resident=resident_1,
                media_url="NA",
                media_start_datetime=(datetime.utcnow() + timedelta(seconds=30)).replace(tzinfo=pytz.utc),
                media_end_datetime=(datetime.utcnow() + timedelta(seconds=60)).replace(tzinfo=pytz.utc),
                media_percent_completed=1,
                media_name="test",
                media_artist="Elvis",
                media_tags="NA",
                media_classification="NA",
                media_features='{"id":"41zpWL98BsYKP5nvtdTM5z","key":0,"uri":"spotify:track:41zpWL98BsYKP5nvtdTM5z","mode":1,"type":"audio_features","tempo":183.178,"energy":0.164,"valence":0.845,"liveness":0.0883,"loudness":-14.579,"track_href":"https://api.spotify.com/v1/tracks/41zpWL98BsYKP5nvtdTM5z","duration_ms":142000,"speechiness":0.0378,"acousticness":0.914,"analysis_url":"https://api.spotify.com/v1/audio-analysis/41zpWL98BsYKP5nvtdTM5z","danceability":0.413,"time_signature":4,"instrumentalness":0.000014}',
                resident_motion='{"history":[0,0,0,0,0,0,1,1,1,1],"percent":0.4,"end_time":"2022-02-21T17:12:15.289328","start_time":"2022-02-21T17:12:04.565609","num_of_seconds":10,"motion_event_pairs":[["2022-02-21T17:12:10.197264","2022-02-21T17:12:14.782564"]],"rolling_history_5sec":[0,0,0,0,0,0,0.2,0.4,0.6,0.8],"rolling_history_10sec":[0,0,0,0,0,0,0,0,0,0.4]}',
            ),
        ]
    )        

def create_mediainteractions():
    models.MediaInteraction.objects.all().delete()

    resident_1 = models.Resident.objects.filter(pk=UUID_1).first()
    resident_2 = models.Resident.objects.filter(pk=UUID_2).first()

    models.MediaInteraction.objects.bulk_create(
        [
            models.MediaInteraction(
                media_interaction_id=UUID_1,
                memorybox_session_media_id=UUID_1,
                resident=resident_1,
                log_datetime=datetime.utcnow().replace(tzinfo=pytz.utc),
                elapsed_seconds=3,
                media_percent_completed=0.01,
                event="prompt",
                data="Let's dance",
            ),
        ]
    )            