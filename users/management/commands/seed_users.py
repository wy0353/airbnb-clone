import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as user_models

category = "users"

class Command(BaseCommand):

    help = f"Create fake {category}"

    def add_arguments(self, parser):
        parser.add_argument("--count", default=1, type=int, help=f"How many {category} create want?")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]

        seeder = Seed.seeder()
        seeder.add_entity(user_models.User, count, {
            "is_staff": False,
            "is_superuser": False,
            "gender": lambda x: random.choice([
                "male", "female", "other",
            ]),
            "language": lambda x: random.choice([
                "ko", "en",
            ]),
            "currency": lambda x: random.choice([
                "krw", "usd",
            ]),
            "avatar": lambda x: f"icons/animals/{random.randint(1, 26)}.png",
        })
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{count} {category} created!"))
