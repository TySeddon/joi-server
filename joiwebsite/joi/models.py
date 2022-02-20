from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# make email address unique
User._meta.get_field('email')._unique = True

class Resident(models.Model):
    """
    Represents a Resident
    """
    resident_id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True) # may or may not be associated with user
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    is_active = models.BooleanField(null=False) # gives admin ability to disable (not currently using this)
    knowledge_base_name = models.CharField(max_length=50, null=True)

class CarePartner(models.Model):
    """
    Represents a Care Partner
    """
    carepartner_id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True) # may or may not be associated with user
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    is_active = models.BooleanField(null=False) # gives admin ability to disable (not currently using this)

class CarePartnerResident(models.Model):
    """
    Represents relationship between Care Partner and Resident.
    A Care Partner can be associated with multiple Residents and/or
    a Resident can be associated with multiple Care Parnters
    """
    carepartner_resident_id = models.UUIDField(primary_key=True)
    carepartner = models.ForeignKey(CarePartner, on_delete=models.DO_NOTHING, null=False)
    resident = models.ForeignKey(Resident, on_delete=models.DO_NOTHING, null=False)

class Device(models.Model):
    """
    Represents a Joi Device (Raspberry Pi)
    """
    device_id = models.UUIDField(primary_key=True)  # Joi (Raspberry Pi) should store this in /etc/environment
    name = models.CharField(max_length=50, null=False) 
    description = models.CharField(max_length=255, null=True) 
    resident = models.ForeignKey(Resident, on_delete=models.DO_NOTHING, null=False) # the resident currently associated with this device
    is_active = models.BooleanField(null=False) # gives admin ability to disable  (not currently using this)

class MemoryBoxType(models.Model):
    """
    Represents a type of memory box (music, photo, etc)
    """
    memorybox_type_id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50, null=False) 
    description = models.CharField(max_length=255, null=True) 

class MemoryBox(models.Model):
    """
    Represents a collection of media items
    A Resident can have multiple memory boxes
    Each memory box holds one kind of media (music or photos)
    A memory box is associated with either a Spotify playlist or a Google Photos album
    NOTE: users and researchers may refer to a single memory box with different folders or libraries
    within that one memory box.  In that context, this class is that folder or library.
    """
    memorybox_id = models.UUIDField(primary_key=True)
    memorybox_type = models.ForeignKey(MemoryBoxType, on_delete=models.DO_NOTHING, null=False)
    resident = models.ForeignKey(Resident, on_delete=models.DO_NOTHING, null=False)
    name = models.CharField(max_length=50, null=False) 
    description = models.CharField(max_length=255, null=True) 
    url = models.CharField(max_length=2048, null=False)  # reference to spotify playlist or google photos library/album
    tags = models.CharField(max_length=255, null=True) # comma delimited list?
    is_active = models.BooleanField(null=False) # gives admin, researcher, or care partner ability to disable  (not currently using this)

class MemoryBoxSession(models.Model):
    """
    Represents a Resident's session with a memory box
    A session has a specific start and end 
    """
    memorybox_session_id = models.UUIDField(primary_key=True)
    memorybox = models.ForeignKey(MemoryBox, on_delete=models.DO_NOTHING, null=False)
    resident = models.ForeignKey(Resident, on_delete=models.DO_NOTHING, null=False)  # this breaks a rule of normalization.  Including it to keep it simpler for researchers to query
    device = models.ForeignKey(Device, on_delete=models.DO_NOTHING, null=False)
    session_start_method = models.CharField(max_length=50, null=False)  # how started
    session_end_method = models.CharField(max_length=50, null=True)  # how ended (naturally, error, or stopped by resident)
    session_start_datetime = models.DateTimeField(null=False)
    session_end_datetime = models.DateTimeField(null=True)
    resident_self_reported_feeling = models.CharField(max_length=50, null=True)  # recorded at end of session
    carepartner_flag = models.BooleanField(null=False, default=False)  # care partner can flag this for follow-up
    researcher_flag = models.BooleanField(null=False, default=False) # researcher can flag this for follow-up
    researcher_notes = models.CharField(max_length=1024, null=True)

class MemoryBoxSessionMedia(models.Model):
    """
    Represents the playing of a media item (song, photo, video, etc) 
    within the context of a MemmoryBoxSession
    """
    memorybox_session_media_id = models.UUIDField(primary_key=True)
    memorybox_session = models.ForeignKey(MemoryBoxSession, on_delete=models.DO_NOTHING, null=False)
    resident = models.ForeignKey(Resident, on_delete=models.DO_NOTHING, null=False)  # this breaks a rule of normalization.  Including it to keep it simpler for researchers to query
    media_url = models.CharField(max_length=2048, null=False)
    media_start_datetime = models.DateTimeField(null=False)
    media_end_datetime = models.DateTimeField(null=True)
    media_percent_completed = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    media_name = models.CharField(max_length=255, null=False)
    media_artist = models.CharField(max_length=255, null=False)
    media_tags = models.CharField(max_length=255, null=True) # comma delimited list?
    media_classification = models.CharField(max_length=255, null=True)    # what did Spotify say about this song
    resident_motion = models.JSONField(max_length=2048, null=True)    # was resident moving and how much?
    resident_utterances = models.CharField(max_length=1024, null=True) # stuff said by resident
    resident_self_reported_feeling = models.CharField(max_length=50, null=True)  # recorded at end of song
    carepartner_flag = models.BooleanField(null=False, default=False)  # care partner can flag this for follow-up
    researcher_flag = models.BooleanField(null=False, default=False) # researcher can flag this for follow-up
    researcher_notes = models.CharField(max_length=1024, null=True)

class MediaInteraction(models.Model):
    """
    Represents the interaction between a Resident and Media
    within the context of a MemmoryBoxSession
    While media is playing, Joi will periodically collect data such as:
        was the Resident moving, did they request it to stop, did they saying something, did they make facial expressions
    """
    media_interaction_id = models.UUIDField(primary_key=True)
    memorybox_session_media = models.ForeignKey(MemoryBoxSessionMedia, on_delete=models.DO_NOTHING, null=False)
    resident = models.ForeignKey(Resident, on_delete=models.DO_NOTHING, null=False)  # this breaks a rule of normalization.  Including it to keep it simpler for researchers to query
    log_datetime = models.DateTimeField(null=False)
    elapsed_seconds = models.IntegerField(null=False, default=0)
    media_percent_completed = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    event = models.CharField(max_length=50, null=False)  # stopped, motion, utterance, facial expression
    data = models.CharField(max_length=2048, null=True)  # movement data, utterance text, or facial expression data (JSON?)
    carepartner_flag = models.BooleanField(null=False, default=False)  # care partner can flag this for follow-up
    researcher_flag = models.BooleanField(null=False, default=False) # researcher can flag this for follow-up
    researcher_notes = models.CharField(max_length=1024, null=True)

class Slideshow(models.Model):
    """Table to facilitate communication between Joi device (Raspberry Pi) and Slideshow (web page server from Joi Server)"""
    slideshow_id = models.UUIDField(primary_key=True)
    media_id = models.CharField(max_length=255, null=False)  # google photo mediaItem.id
    media_url = models.CharField(max_length=2048, null=False) # google photo mediaItem.baseUrl
    tick_count = models.IntegerField(null=False)
    ping_datetime = models.DateTimeField(null=False)

