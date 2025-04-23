

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
    # permission_classes = [IsAuthenticated]
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

#лайк
class LikeTrackAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, track_id):
        try:
            track = Track.objects.get(id=track_id)
        except Track.DoesNotExist:
            return Response({'error': 'Трек не найден'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if user in track.likes.all():
            track.likes.remove(user)
            liked = False
        else:
            track.likes.add(user)
            liked = True

        return Response({
            'liked': liked,
            'like_count': track.likes.count()  # или track.like_count()
        })
    

# за лайканные музыки
class LikedTracksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        liked_tracks = request.user.liked_tracks.all()  # related_name в ManyToMany
        serializer = TrackSerializer(liked_tracks, many=True)
        return Response(serializer.data)



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
    search_fields = ['username']


# Треки
from rest_framework.exceptions import PermissionDenied

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
    

    def destroy(self, request, *args, **kwargs):
        # Получаем объект трека
        track = self.get_object()

        # Проверяем, является ли текущий пользователь владельцем
        if track.owner != request.user:
            raise PermissionDenied("Вы не можете удалить этот трек, потому что вы не являетесь его владельцем.")

        # Если проверка пройдена, удаляем трек
        track.delete()
        return Response({"message": "Трек успешно удален"}, status=status.HTTP_204_NO_CONTENT)



class UserTracksView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrackSerializer

    def get_queryset(self):
        return Track.objects.filter(owner=self.request.user)
# удаление
class DeleteTrackAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, track_id):
        try:
            track = Track.objects.get(id=track_id)
        except Track.DoesNotExist:
            return Response({'error': 'Трек не найден'}, status=status.HTTP_404_NOT_FOUND)

        if track.owner != request.user:
            raise PermissionDenied("Вы не можете удалить этот трек.")

        track.delete()
        return Response({"message": "Трек успешно удален"}, status=status.HTTP_204_NO_CONTENT)









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

    @action(detail=False, methods=['get'])
    def created_tracks(self, request):
        # Получаем все треки, которые были созданы текущим пользователем
        created_tracks = Track.objects.filter(owner=request.user)
        serializer = TrackSerializer(created_tracks, many=True)
        return Response(serializer.data)





class LikedTracksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        liked_tracks = request.user.liked_tracks.all()  # related_name
        serializer = TrackSerializer(liked_tracks, many=True)
        return Response(serializer.data)
    

class OtherProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Проверка аутентификации

    def get(self, request, user_id):
        try:
            user_profile = UserProfile.objects.get(user__id=user_id)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found."}, status=404)

class LikedTracksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            liked_tracks = user.liked_tracks.all()  # Получаем залайканные треки пользователя
            serializer = TrackSerializer(liked_tracks, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)
        















class CreatedTracksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Получаем треки, у которых owner равен текущему пользователю
        created_tracks = Track.objects.filter(owner=request.user)
        serializer = TrackSerializer(created_tracks, many=True)
        return Response(serializer.data)
