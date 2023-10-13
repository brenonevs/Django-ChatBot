# Generated by Django 4.2.5 on 2023-10-13 23:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatbot', '0002_conversation_alter_character_id_usermessage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
