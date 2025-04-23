
# music/models.py

from django.db import models
from django.contrib.auth.models import User


class Track(models.Model):
  title = models.CharField(max_length=100)
  artist = models.CharField(max_length=100)
  album = models.CharField(max_length=100, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  image = models.ImageField(upload_to='track_images/', blank=True, null=True)
  audio = models.FileField(upload_to='track_audios/', blank=True, null=True)
  owner = models.ForeignKey(User, on_delete=models.CASCADE)


  likes = models.ManyToManyField(User, related_name="liked_tracks", blank=True)

  def like_count(self):
    return self.likes.count()

  def __str__(self):
    return f"{self.title} by {self.artist}"


class Playlist(models.Model):
  name = models.CharField(max_length=255)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")

  tracks = models.ManyToManyField(Track, related_name="in_playlists", blank=True)
  likes = models.ManyToManyField(User, related_name="liked_playlists", blank=True)

  def like_count(self):
    return self.likes.count()

  def __str__(self):
    return self.name




from django.db import models
from django.contrib.auth.models import User


class SearchList(models.Model):
  name = models.CharField(max_length=255)
  musics = models.ManyToManyField(Track, related_name="in_searches", blank=True)

  def __str__(self):
    return self.name


# music/models.py

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def liked_tracks(self):
        return self.user.liked_tracks.all()

    def liked_playlists(self):
        return self.user.liked_playlists.all()

    def __str__(self):
        return f"{self.user.username}'s profile"
