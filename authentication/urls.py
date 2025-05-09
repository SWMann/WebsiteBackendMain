 
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import DiscordOAuthView, LogoutView, UserProfileView

urlpatterns = [
    path('discord/', DiscordOAuthView.as_view(), name='discord-oauth'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
]