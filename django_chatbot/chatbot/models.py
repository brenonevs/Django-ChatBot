from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Character(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    prompt = models.TextField()
    chat_model_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation between {self.user} and {self.character}"


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    conversation = models.ForeignKey(Conversation, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        abstract = True


class UserMessage(Message):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class CharacterMessage(Message):
    sender = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True)
