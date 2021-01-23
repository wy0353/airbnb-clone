import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models

category = "rooms"

class Command(BaseCommand):

    help = f"Create fake {category}"

    def add_arguments(self, parser):
        parser.add_argument("--count", default=1, type=int, help=f"How many {category} create want?")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]

        room_types = room_models.RoomType.objects.all()
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        house_rules = room_models.HouseRule.objects.all()
        users = user_models.User.objects.all()        
        images = [
            "https://images.unsplash.com/photo-1481277542470-605612bd2d61?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MXx8cm9vbXxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1486946255434-2466348c2166?ixid=MXwxMjA3fDB8MHxzZWFyY2h8Mnx8cm9vbXxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?ixid=MXwxMjA3fDB8MHxzZWFyY2h8M3x8cm9vbXxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1486304873000-235643847519?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NHx8cm9vbXxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1564078516393-cf04bd966897?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NXx8cm9vbXxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1554995207-c18c203602cb?ixid=MXwxMjA3fDB8MHxzZWFyY2h8Nnx8cm9vbXxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1560448205-4d9b3e6bb6db?ixid=MXwxMjA3fDB8MHxzZWFyY2h8OHx8cm9vbXxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1589834390005-5d4fb9bf3d32?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTN8fHJvb218ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1463797221720-6b07e6426c24?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTR8fHJvb218ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1484101403633-562f891dc89a?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTV8fHJvb218ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1537726235470-8504e3beef77?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTl8fHJvb218ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1513161455079-7dc1de15ef3e?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTZ8fHJvb218ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1552242718-c5360894aecd?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MjJ8fHJvb218ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MjF8fHJvb218ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1506730447-7683abca8434?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MjV8fHJvb218ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1553881651-43348b2ca74e?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MjZ8fHJvb218ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1484154218962-a197022b5858?ixid=MXwxMjA3fDB8MHxzZWFyY2h8Mjd8fHJvb218ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1546967900-1bea5f16b69d?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MzB8fHJvb218ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1470290378698-263fa7ca60ab?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MzF8fHJvb218ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MzZ8fHJvb218ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1533008093099-e2681382639a?ixid=MXwxMjA3fDB8MHxzZWFyY2h8Mzd8fHJvb218ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1572891086295-6c1c7c476549?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NDJ8fHJvb218ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1589911057171-44545e48c56b?ixid=MXwxMjA3fDB8MHxzZWFyY2h8Mzl8fHJvb218ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
        ]

        seeder = Seed.seeder()
        seeder.add_entity(room_models.Room, count, {
            "name": lambda x: seeder.faker.address(),
            "host": lambda x: random.choice(users),
            "room_type": lambda x: random.choice(room_types),
            "guests": lambda x: random.randint(1, 20),
            "price": lambda x: random.randint(1, 300),
            "beds": lambda x: random.randint(1, 5),
            "bedrooms": lambda x: random.randint(1, 5),
            "baths": lambda x: random.randint(1, 5),
        })
        rooms_pk = seeder.execute()
        cleaned_rooms_pk = flatten(list(rooms_pk.values()))
        for pk in cleaned_rooms_pk:
            room = room_models.Room.objects.get(pk=pk)

            # amenities
            amenities_select_num = random.randint(5, amenities.count())
            selected_amenities = random.choices(amenities, k=amenities_select_num)
            for a in selected_amenities:
                room.amenities.add(a)

            # facilities
            facilities_select_num = random.randint(5, facilities.count())
            selected_facilities = random.choices(facilities, k=facilities_select_num)
            for a in selected_facilities:
                room.facilities.add(a)

            # house rules
            house_rules_select_num = random.randint(5, house_rules.count())
            selected_house_rules = random.choices(house_rules, k=house_rules_select_num)
            for a in selected_house_rules:
                room.house_rules.add(a)

            # photos
            photos_create_num = random.randint(4, 10)
            for i in range(0, photos_create_num):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    url=random.choice(images),
                    room=room,
                )

        self.stdout.write(self.style.SUCCESS(f"{count} {category} created!"))
