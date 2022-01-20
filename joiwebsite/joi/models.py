from django.db import models

class Resident(models.Model):
    resident_id = models.UUIDField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    