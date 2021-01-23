from django.core.management.base import BaseCommand
from rooms import models as room_models

category = "house rules"

class Command(BaseCommand):

    help = f"Create fake {category}"

    def handle(self, *args, **kwargs):
        items = [
            "Don't smoke",
            "No pet",
            "No party",
            "No event",
            "Self check in by keypad",
            "Check in/out time",
        ]
        
        count_created = 0
        for item in items:
            try:
                room_models.HouseRule.objects.get(name=item)
                continue
            except room_models.HouseRule.DoesNotExist:
                room_models.HouseRule.objects.create(name=item)
                count_created += 1

        self.stdout.write(self.style.SUCCESS(f"{count_created} {category} created!"))
