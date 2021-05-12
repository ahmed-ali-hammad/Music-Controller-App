from django.db import models
from api.models import *

class SpotifyToken(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    access_token = models.CharField(max_length = 150)
    refresh_token = models.CharField(max_length = 150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length = 50)

    class Meta:
        verbose_name = "Spotify Token"
        verbose_name_plural = "Spotify Tokens"
