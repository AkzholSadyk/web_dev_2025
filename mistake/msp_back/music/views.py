

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters, viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated



from .models import Track, Playlist, UserProfile
from .serializers import (
    RegisterSerializer,
    TrackSerializer,
    PlaylistSerializer,
    UserSerializer,
    UserProfileSerializer,
)



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Поиск треков
class TrackSearchView(ListAPIView):
    queryset = Track.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TrackSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'artist', 'album']


# Поиск плейлистов
class PlaylistSearchView(ListAPIView):
    queryset = Playlist.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PlaylistSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


# Поиск пользователей
class UserSearchView(ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']


# Треки
class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TrackSerializer

    def perform_create(self, serializer):
      if self.request.user.is_authenticated:
        serializer.save(owner=self.request.user)
      else:
        anonymous_user, created = User.objects.get_or_create(username='anonymous')
        serializer.save(owner=anonymous_user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        track = self.get_object()
        track.likes.add(request.user)
        return Response({'status': 'liked'})

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        track = self.get_object()
        track.likes.remove(request.user)
        return Response({'status': 'unliked'})


# Плейлисты
class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PlaylistSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        playlist = self.get_object()
        playlist.likes.add(request.user)
        return Response({'status': 'liked'})

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        playlist = self.get_object()
        playlist.likes.remove(request.user)
        return Response({'status': 'unliked'})






class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
