from django.core.management.base import BaseCommand
import joi.data as data

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data.delete_data()
