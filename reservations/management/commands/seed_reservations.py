import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations import models as reservation_models
from rooms import models as room_models
from users import models as user_models


category = "reservations"


class Command(BaseCommand):

    help = f"Create fake {category}"

    def add_arguments(self, parser):
        parser.add_argument("--count", default=1, type=int, help=f"How many {category} create want?")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]

        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        
        seeder = Seed.seeder()
        seeder.add_entity(reservation_models.Reservation, count, {
            "status": lambda x: random.choice([
                "pending", "confirmed", "canceled",
            ]),
            "check_in": lambda x: datetime.now(),
            "check_out": lambda x: datetime.now() + timedelta(days=random.randint(3, 25)),
            "guest": lambda x: random.choice(users),
            "room": lambda x: random.choice(rooms),
        })
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{count} {category} created!"))
