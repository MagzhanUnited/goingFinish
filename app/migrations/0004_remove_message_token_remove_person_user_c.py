# Generated by Django 4.1.5 on 2023-03-19 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_message_token_alter_person_user_c'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='token',
        ),
        migrations.RemoveField(
            model_name='person',
            name='user_c',
        ),
    ]
