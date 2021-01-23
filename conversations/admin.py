from django.contrib import admin
from . import models as conversation_models


@admin.register(conversation_models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ Conversation Admin Definition """

    list_display = (
        "__str__",
        "count_messages",
        "count_participants",
    )


@admin.register(conversation_models.Message)
class MessageAdmin(admin.ModelAdmin):

    """ Message Admin Definition """

    list_display = (
        "__str__",
        "created",
    )
