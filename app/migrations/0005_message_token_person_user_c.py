# Generated by Django 4.1.5 on 2023-03-19 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_message_token_remove_person_user_c'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='token',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='user_c',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
