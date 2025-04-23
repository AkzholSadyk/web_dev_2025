from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    TrackViewSet,
    PlaylistViewSet,
    TrackSearchView,
    PlaylistSearchView,
    UserSearchView,
    LikeTrackAPIView,
    LikedTracksAPIView,
    OtherProfileView,
    LikedTracksView,
    CreatedTracksAPIView,
    DeleteTrackAPIView,

)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserProfileView


router = DefaultRouter()
# router.register('tracks', TrackViewSet)
# router.register('playlists', PlaylistViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Создание трека и плейлиста
    path('create-tracks/', TrackViewSet.as_view({'post': 'create'}), name='create_tracks'),
    path('create-playlists/', PlaylistViewSet.as_view({'post': 'create'}), name='create_playlists'),

    #other
    path('users/<int:user_id>/', OtherProfileView.as_view(), name='other-profile'),
    path('users/<int:user_id>/liked-tracks/', LikedTracksView.as_view(), name='other-liked-tracks'),


    # Поиск
    path('search/tracks/', TrackSearchView.as_view(), name='search-tracks'),
    path('tracks/<int:track_id>/like/', LikeTrackAPIView.as_view()),
    path('profile/liked-tracks/', LikedTracksAPIView.as_view(), name='liked-tracks'),
    path('search/playlists/', PlaylistSearchView.as_view(), name='search-playlists'),
    path('search/users/', UserSearchView.as_view(), name='search-users'),

    # Основные ресурсы
    path('', include(router.urls)),

    # profile of user
    path('profile/', UserProfileView.as_view(), name='user-profile'),


    # удаление
    path('profile/created_tracks/', CreatedTracksAPIView.as_view(), name='created-tracks'),
    path('delete-track/<int:track_id>/', DeleteTrackAPIView.as_view(), name='delete-track'),
    
]
