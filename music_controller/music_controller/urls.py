from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("api.urls", namespace = "api")),
    path('', include("frontend.urls", namespace = "frontend")),
    path('spotify/', include("spotify.urls", namespace = "spotify")),
    
 
]
