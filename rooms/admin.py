from django.contrib import admin
from . import models as room_models

@admin.register(
    room_models.RoomType,    
    room_models.HouseRule,    
    room_models.Amenity,    
    room_models.Facility,    
)
class ItemAdmin(admin.ModelAdmin):

    """ Abstract Item Admin Definition """

    pass


@admin.register(room_models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Room Photo Admin Definition """

    pass


@admin.register(room_models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    pass
