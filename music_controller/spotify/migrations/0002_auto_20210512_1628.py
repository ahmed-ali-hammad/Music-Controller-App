# Generated by Django 3.2 on 2021-05-12 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210503_1636'),
        ('spotify', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spotifytoken',
            options={'verbose_name': 'Spotify Token', 'verbose_name_plural': 'Spotify Tokens'},
        ),
        migrations.RemoveField(
            model_name='spotifytoken',
            name='user',
        ),
        migrations.AddField(
            model_name='spotifytoken',
            name='room',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.room'),
        ),
    ]