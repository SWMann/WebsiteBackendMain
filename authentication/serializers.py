 
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'discord_id', 'avatar_url', 'date_joined', 'last_login']
        read_only_fields = ['id', 'discord_id', 'date_joined', 'last_login']