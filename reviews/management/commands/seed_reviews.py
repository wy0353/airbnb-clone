import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as review_models
from rooms import models as room_models
from users import models as user_models

category = "reviews"

class Command(BaseCommand):

    help = f"Create fake {category}"

    def add_arguments(self, parser):
        parser.add_argument("--count", default=1, type=int, help=f"How many {category} create want?")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]

        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        
        seeder = Seed.seeder()
        seeder.add_entity(review_models.Review, count, {
            "accuracy": lambda x: random.randint(0, 5),
            "communication": lambda x: random.randint(0, 5),
            "cleanliness": lambda x: random.randint(0, 5),
            "location": lambda x: random.randint(0, 5),
            "check_in": lambda x: random.randint(0, 5),
            "value": lambda x: random.randint(0, 5),
            "user": lambda x: random.choice(users),
            "room": lambda x: random.choice(rooms),
        })
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{count} {category} created!"))
