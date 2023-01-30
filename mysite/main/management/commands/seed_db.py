from django.core.management.base import BaseCommand, CommandError
from main.models import Gender

class Command(BaseCommand):
    def handle(self, *args, **options):
        genders = ['f', 'm']
        for gender in genders:
            gender = Gender(
                name = gender
            )

            gender.save()
