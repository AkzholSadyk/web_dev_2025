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
    like_count = serializers.SerializerMethodField()
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Track
        fields = '__all__'
        read_only_fields = ['owner', 'created_at']

    def get_like_count(self, obj):
        return obj.likes.count()

class PlaylistSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Playlist
        fields = '__all__'
        read_only_fields = ['author']


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='userprofile.avatar', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username','first_name', 'last_name', 'avatar']

from .models import UserProfile



class UserProfileSerializer(serializers.ModelSerializer):
    # liked_tracks = TrackSerializer(many=True, read_only=True, source='liked_tracks')
    # liked_playlists = PlaylistSerializer(many=True, read_only=True, source='liked_playlists')
    liked_tracks = TrackSerializer(many=True, read_only=True)
    liked_playlists = PlaylistSerializer(many=True, read_only=True)

    user = UserSerializer(read_only=True)

    username = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['user','avatar', 'username','liked_tracks', 'liked_playlists']

    def get_username(self, obj):
        return obj.user.username
