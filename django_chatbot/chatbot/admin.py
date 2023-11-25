from django.contrib import admin
from .models import Character, UserMessage, CharacterMessage, Conversation

admin.site.register(Character)
admin.site.register(UserMessage)
admin.site.register(CharacterMessage)
admin.site.register(Conversation)
