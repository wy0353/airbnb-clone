from django.contrib import admin
from . import models as conversation_models


@admin.register(conversation_models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ Conversation Admin Definition """

    pass


@admin.register(conversation_models.Message)
class MessageAdmin(admin.ModelAdmin):

    """ Message Admin Definition """

    pass
