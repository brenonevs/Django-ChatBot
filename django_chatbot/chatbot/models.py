from django.db import models


class Character(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    prompt = models.TextField()
    chat_model_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
