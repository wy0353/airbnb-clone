from django.core.management.base import BaseCommand
from rooms import models as room_models

category = "facilities"

class Command(BaseCommand):

    help = f"Create fake {category}"

    def handle(self, *args, **kwargs):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        
        count_created = 0
        for f in facilities:
            try:
                room_models.Facility.objects.get(name=f)
                continue
            except room_models.Facility.DoesNotExist:
                room_models.Facility.objects.create(name=f)
                count_created += 1

        self.stdout.write(self.style.SUCCESS(f"{count_created} {category} created!"))
