from django.core.management.base import BaseCommand
from rooms import models as room_models

category = "amenities"

class Command(BaseCommand):

    help = f"Create fake {category}"

    def handle(self, *args, **kwargs):
        amenities = [
            "Air conditioning",
            "Alarm Clock",
            "Balcony",
            "Bathroom",
            "Bathtub",
            "Bed Linen",
            "Boating",
            "Cable TV",
            "Carbon monoxide detectors",
            "Chairs",
            "Children Area",
            "Coffee Maker in Room",
            "Cooking hob",
            "Cookware & Kitchen Utensils",
            "Dishwasher",
            "Double bed",
            "En suite bathroom",
            "Free Parking",
            "Free Wireless Internet",
            "Freezer",
            "Fridge / Freezer",
            "Golf",
            "Hair Dryer",
            "Heating",
            "Hot tub",
            "Indoor Pool",
            "Ironing Board",
            "Microwave",
            "Outdoor Pool",
            "Outdoor Tennis",
            "Oven",
            "Queen size bed",
            "Restaurant",
            "Shopping Mall",
            "Shower",
            "Smoke detectors",
            "Sofa",
            "Stereo",
            "Swimming pool",
            "Toilet",
            "Towels",
            "TV",
        ]
        
        count_created = 0
        for a in amenities:
            try:
                room_models.Amenity.objects.get(name=a)
                continue
            except room_models.Amenity.DoesNotExist:
                room_models.Amenity.objects.create(name=a)
                count_created += 1

        self.stdout.write(self.style.SUCCESS(f"{count_created} {category} created!"))
