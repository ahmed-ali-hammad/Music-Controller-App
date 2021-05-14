from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from django.shortcuts import redirect
from requests import Request, post, get, put
from .models import *
from rest_framework import status
import os

CLIENT_ID = os.environ["SP_CLIENT_ID"]
CLIENT_SECRET = os.environ["SP_CLIENT_SECRET"]
REDIRECT_URI =  "http://localhost:8000/spotify/redirect"
SPOTIFY_BASE_URL = "https://api.spotify.com/v1/me/"




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


def excute_spotify_api_request(session_id, endpoint, post_ = False, put_ = False):
    token = SpotifyToken.objects.filter(room__host = session_id)[0]
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + token.access_token
    }


    if post_:
        post(SPOTIFY_BASE_URL + endpoint, headers = headers)

    if put_:
        print(token.access_token)
        response = put(SPOTIFY_BASE_URL + endpoint, headers = headers)
        print(response)
        print(response.json())

    response = get (SPOTIFY_BASE_URL + endpoint, {} , headers = headers)

    try: 
        return response.json()
        
    except:
        return {'error': "issue with request"} 


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
                expires_in = timezone.now() + timedelta(seconds = response['expires_in'])
                token_type = response['token_type']

                create_or_update_token(session_id, access_token, refresh_token, token_type, expires_in)

            return Response({"status": True})
        return Response({"status": False})



class CurrentSongAPIView(APIView):
    def get(self, request):

        room_code = self.request.session['room_code']    
        rooms = Room.objects.filter(code = room_code)
        if rooms.exists():
            room = rooms[0]
        else: 
            return Response ({'Message': "there is no room"}, status = status.HTTP_404_NOT_FOUND)
        
        session_id = room.host
        endpoint = "player/currently-playing/"
        response = excute_spotify_api_request(session_id, endpoint)

        if 'error' in response or 'item' not in response:
            return Response({'response': response}, status= status.HTTP_204_NO_CONTENT) 

        item = response['item']
        duration = item['duration_ms']
        progress = response['progress_ms']
        album_cover = item['album']['images'][0]['url']
        is_playing = response['is_playing']
        song_id = item ['id']

        artist_string = ""

        for i, artist in enumerate(item['artists']):
            if i > 0:
                artist_string += ", "
            name = artist['name']
            artist_string += name
        
        song = {
            'title': item['name'],
            'artist': artist_string,
            'duration': duration,
            'time': progress,
            'image_url': album_cover,
            'is_playing': is_playing,
            'votes': 0,
            'id': song_id,

        }
        return Response (song)
        

class PauseSongAPIView(APIView):
    def put(self, request):
        room_code = self.request.session['room_code']
        room = Room.objects.filter(code = room_code)[0]
        if self.request.session.session_key == room.host or room.guest_can_pause:
            excute_spotify_api_request(room.host, 'player/play/', put_= True)
            return Response({}, status = status.HTTP_204_NO_CONTENT)
        return Response ({} ,status = status.HTTP_403_FORBIDDEN)


class PlaySongAPIView(APIView):
    def put(self, request):
        room_code = self.request.session['room_code']
        room = Room.objects.filter(code = room_code)[0]
        if self.request.session.session_key == room.host or room.guest_can_pause:
            excute_spotify_api_request(room.host, 'player/pause/', put_= True)
            return Response({}, status = status.HTTP_204_NO_CONTENT)
        return Response ({} ,status = status.HTTP_403_FORBIDDEN)