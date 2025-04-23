import { Component, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'api-view-profile',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './view-profile.component.html',
  styleUrls: ['./view-profile.component.css']
})
export class ViewProfileComponent{
  private route = inject(ActivatedRoute);
  private http = inject(HttpClient);

  userId: number;
  user: any = {};
  likedTracks: any[] = [];
  defaultAvatar = 'http://localhost:8000/media/avatars/default-avatar.png';


  constructor() {
    this.userId = +this.route.snapshot.paramMap.get('id')!;
    this.fetchUserProfile();
    this.fetchLikedTracks();
  }

  fetchUserProfile() {
    const token = localStorage.getItem('access_token');
    if (token) {
      const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
      this.http.get<any>(`http://localhost:8000/music/api/users/${this.userId}/`, { headers })
        .subscribe(
          (response) => {
            this.user = response;
          },
          (error) => {
            console.error('Error fetching user profile:', error);
            alert('Ошибка при загрузке профиля пользователя.');
          }
        );
    } else {
      console.log('No token found, redirecting to login...');
      alert('Необходимо войти в систему для доступа к данным.');
    }
  }

  fetchLikedTracks() {
    const token = localStorage.getItem('access_token');
    if (token) {
      const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
      this.http.get<any[]>(`http://localhost:8000/music/api/users/${this.userId}/liked-tracks/`, { headers })
        .subscribe(
          (response) => {
            this.likedTracks = response;
          },
          (error) => {
            console.error('Error fetching liked tracks:', error);
          }
        );
    }
  }

  likeTrack(trackId: number) {
    const token = localStorage.getItem('access_token');
    if (token) {
      const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
      this.http.post(`http://localhost:8000/music/api/tracks/${trackId}/like/`, {}, { headers })
        .subscribe({
          next: () => {
            console.log(`Трек ${trackId} лайкнут.`);
            this.fetchLikedTracks(); // Обновим список лайков
          },
          error: (err) => {
            console.error('Ошибка при лайке трека:', err);
          }
        });
    } else {
      alert('Необходимо войти в систему.');
    }
  }
  
}
