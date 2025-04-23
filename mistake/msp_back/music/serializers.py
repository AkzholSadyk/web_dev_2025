from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Track, Playlist



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        # Создание профиля вручную
        from .models import UserProfile
        UserProfile.objects.create(user=user)
        return user



class TrackSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    likes = serializers.PrimaryKeyRelatedField(
       many=True, read_only=True
    )

    class Meta:
        model = Track
        fields = '__all__'
        read_only_fields = ['owner', 'created_at']


class PlaylistSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Playlist
        fields = '__all__'
        read_only_fields = ['author']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']




from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    liked_tracks = TrackSerializer(many=True, read_only=True, source='liked_tracks')
    liked_playlists = PlaylistSerializer(many=True, read_only=True, source='liked_playlists')

    class Meta:
        model = UserProfile
        fields = ['avatar', 'liked_tracks', 'liked_playlists']
