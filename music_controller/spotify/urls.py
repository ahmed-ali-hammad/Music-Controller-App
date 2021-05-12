from django.urls import path
from .views import *

app_name = "spotify"

urlpatterns = [
    path('get/auth/url/', AuthURL.as_view()),
    path('redirect/', spotify_callback, name = "redirect"),
    path('is/authenticated/', IsAuthenticatedAPIView.as_view()),
]