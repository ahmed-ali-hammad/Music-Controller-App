from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from django.shortcuts import redirect
from requests import Request, post
from django.urls import reverse_lazy
from .models import *
import os

CLIENT_ID = os.environ["SP_CLIENT_ID"]
CLIENT_SECRET = os.environ["SP_CLIENT_SECRET"]
REDIRECT_URI =  "http://localhost:8000/spotify/redirect"

def create_or_update_token(session_id, access_token, refresh_token, token_type, expires_in):
    room_token = SpotifyToken.objects.filter (room__host = session_id)
    if room_token.exists():
        room_token = room_token[0]

        room_token.access_token = access_token
        room_token.refresh_token = refresh_token
        room_token.expires_in = timezone.now() + timedelta(seconds = expires_in)
        room_token.token_type = token_type

        room_token.save(update_fields= ["access_token", "refresh_token", "expires_in", "token_type"]) 

    else:
        room_token = SpotifyToken(
            room = Room.objects.get(host = session_id),
            access_token = access_token,
            refresh_token = refresh_token,
            expires_in = timezone.now() + timedelta(seconds = expires_in),
            token_type = token_type
                )

        room_token.save()


class AuthURL(APIView):
    def get(self, request):
        scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

        print(REDIRECT_URI)

        url = Request('GET', "https://accounts.spotify.com/authorize", params= {
            'scope': scope,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url
        return Response ({'url': url})


def spotify_callback(request):
    code = request.GET['code'] 

    response = post("https://accounts.spotify.com/api/token", data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    print(response)

    token_type = response['token_type']
    access_token = response['access_token']
    refresh_token = response['refresh_token']
    expires_in = response['expires_in']

    if not request.session.exists(request.session.session_key):
            request.session.create()

    session_id = request.session.session_key

    create_or_update_token(session_id, access_token, refresh_token, token_type, expires_in)

    return redirect ("frontend:home")

class IsAuthenticatedAPIView(APIView):
    def get(self, request):
        if not request.session.exists(request.session.session_key):
            request.session.create()

        session_id = self.request.session.session_key

        tokens = SpotifyToken.objects.filter(room__host = session_id)

        if tokens.exists():
            token = tokens[0]
            if token.expires_in <= timezone.now():
                refresh_token = token.refresh_token

                response = post('https://accounts.spotify.com/api/token', data = {
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET}).json

                access_token = response['access_token']
                refresh_token = response['refresh_token']
                expires_in = datetime.now() + timedelta(seconds = response['expires_in'])
                token_type = response['token_type']

                create_or_update_token(session_id, access_token, refresh_token, token_type, expires_in)

            return Response({"status": True})
        return Response({"status": False})



