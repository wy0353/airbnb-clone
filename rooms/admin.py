from django.contrib import admin
from . import models as room_models
from helpers.django.admin.utils import url_to_html_img

@admin.register(
    room_models.RoomType,    
    room_models.HouseRule,    
    room_models.Amenity,    
    room_models.Facility,    
)
class ItemAdmin(admin.ModelAdmin):

    """ Abstract Item Admin Definition """

    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.rooms.count()

    pass


@admin.register(room_models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Room Photo Admin Definition """

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    def get_thumbnail(self, obj):
        if bool(obj.file):
            return url_to_html_img(obj.file.url)
        
        if bool(obj.url):
            return url_to_html_img(obj.url)

    get_thumbnail.short_description = "Thumbnail"


class PhotoInline(admin.TabularInline):

    """ Photo Inline Definition """

    model = room_models.Photo
    extra = 0


@admin.register(room_models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    fieldsets = (
        ("Main Info", {
            'fields': (
                "name",
                "country",
                "city",
                "address",
                "price",
            ),
        }),
        ("Times", {
            'fields': (
                "check_in",
                "check_out",
                "instant_book",
            ),
        }),
        ("Spaces", {
            'fields': (
                "guests",
                "beds",
                "bedrooms",
                "baths",
            ),
        }),
        ("More About", {
            "classes": (
                "collapse",
            ),
            'fields': (
                "house_rules",
                "amenities",
                "facilities",
            ),
        }),
        ("Last Details", {
            'fields': (
                "host",
                "room_type",
            ),
        }),
    )

    list_display = (
        "name",
        "country",
        "city",
        "address",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "instant_book",
        "city",
        "host__superhost",
        "room_type",
        "house_rules",
        "amenities",
        "facilities",
        "country",
    )

    raw_id_fields = (
        "host",
        "room_type",
    )

    search_fields = (
        "^name", "^host__username", "city", "^country",
    )

    filter_horizontal = (
        "house_rules",
        "amenities",
        "facilities",
    )

    ordering = (
        "name", "price",
    )

    inlines = (
        PhotoInline,
    )

    def count_amenities(self, obj):
        return obj.amenities.count()
    count_amenities.short_description = "Amenities"


    def count_photos(self, obj):
        return obj.photos.count()
    count_photos.short_description = "Photos"
