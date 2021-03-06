from django.utils import timezone
from django.db import models
from django.shortcuts import reverse
from core import models as core_models
from django_countries.fields import CountryField
from custom_calendar import Calendar


class Item(core_models.DefaultModel):

    """ Abstract Item Model Definition """

    class Meta:
        abstract = True

    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class RoomType(Item):

    """ Room Type Item Model Definition """

    class Meta:
        verbose_name = "Room Type"

    pass


class HouseRule(Item):

    """ House Rule Item Model Definition """

    class Meta:
        verbose_name_plural = "House Rules"

    pass


class Amenity(Item):

    """ Amenity Item Model Definition """

    class Meta:
        verbose_name_plural = "Amenities"

    pass


class Facility(Item):

    """ Facility Item Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"

    pass


class Photo(core_models.DefaultModel):

    """ Room Photo Model Definition """

    caption = models.CharField(max_length=80, null=True, blank=True, default=None)
    file = models.ImageField(upload_to="room_photos", null=True, blank=True)
    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name="photos")

    def __str__(self):
        return self.caption


class Room(core_models.DefaultModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField(null=True, blank=True, default=None)
    country = CountryField()
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=140)
    price = models.IntegerField(default=0)
    guests = models.IntegerField(default=0)
    beds = models.IntegerField(default=0)
    bedrooms = models.IntegerField(default=0)
    baths = models.IntegerField(default=0)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="rooms")
    room_type = models.ForeignKey("RoomType", on_delete=models.SET_NULL, related_name="rooms", null=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def get_total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
                
            return round(all_ratings / len(all_reviews), 2)
        return 0

    def get_first_photo(self):
        try:
            photo, = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        return self.photos.all()[1:5]

    def get_calendars(self):
        now = timezone.now()
        year = now.year
        this_month = now.month
        this_month_cal = Calendar(year, this_month)
        next_month = this_month + 1
        if this_month == 12:
            next_month = 1
        next_month_cal = Calendar(year, next_month)
        return [this_month_cal, next_month_cal]
