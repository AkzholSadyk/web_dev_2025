from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    TrackViewSet,
    PlaylistViewSet,
    TrackSearchView,
    PlaylistSearchView,
    UserSearchView,
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

    # Поиск
    path('search/tracks/', TrackSearchView.as_view(), name='search-tracks'),
    path('search/playlists/', PlaylistSearchView.as_view(), name='search-playlists'),
    path('search/users/', UserSearchView.as_view(), name='search-users'),

    # Основные ресурсы
    path('', include(router.urls)),

    # profile of user
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
