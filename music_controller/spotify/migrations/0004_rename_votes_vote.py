# Generated by Django 3.2 on 2021-05-15 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_room_current_song'),
        ('spotify', '0003_votes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Votes',
            new_name='Vote',
        ),
    ]