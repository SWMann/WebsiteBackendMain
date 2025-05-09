import requests
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer


class DiscordOAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get('code')

        if not code:
            return Response({'error': 'Authorization code is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange code for token with Discord
        token_url = f"{settings.DISCORD_API_ENDPOINT}/oauth2/token"
        token_data = {
            'client_id': settings.DISCORD_CLIENT_ID,
            'client_secret': settings.DISCORD_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.DISCORD_REDIRECT_URI,
        }

        token_response = requests.post(token_url, data=token_data)

        if token_response.status_code != 200:
            return Response(
                {'error': 'Failed to get token from Discord', 'details': token_response.json()},
                status=status.HTTP_400_BAD_REQUEST
            )

        token_json = token_response.json()
        access_token = token_json['access_token']

        # Get user info from Discord
        user_url = f"{settings.DISCORD_API_ENDPOINT}/users/@me"
        headers = {'Authorization': f"Bearer {access_token}"}

        user_response = requests.get(user_url, headers=headers)

        if user_response.status_code != 200:
            return Response(
                {'error': 'Failed to get user info from Discord', 'details': user_response.json()},
                status=status.HTTP_400_BAD_REQUEST
            )

        discord_user = user_response.json()

        # Process Discord user info
        discord_id = discord_user['id']
        username = discord_user['username']
        email = discord_user.get('email')

        # Generate avatar URL if available
        avatar_url = None
        if discord_user.get('avatar'):
            avatar_hash = discord_user['avatar']
            avatar_url = f"https://cdn.discordapp.com/avatars/{discord_id}/{avatar_hash}.png"

        # Find or create user
        try:
            user = User.objects.get(discord_id=discord_id)
            # Update user info
            user.username = username
            user.email = email
            user.avatar_url = avatar_url
            user.last_login = timezone.now()
            user.save()
        except User.DoesNotExist:
            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                discord_id=discord_id,
                avatar_url=avatar_url,
                last_login=timezone.now()
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # In JWT-based auth, the client typically just discards the tokens,
        # but we could implement token blacklisting here if needed
        return Response({'success': True})


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)