import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { DatePipe } from '@angular/common';  // Import DatePipe

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css'],
  providers: [DatePipe]  // Provide DatePipe to the component
})
export class ProfileComponent implements OnInit {
  profile: any = null;
  username = '';
  likedTracks: any[] = [];
  createdTracks: any[] = []; // Добавляем переменную для созданных треков
  defaultAvatar = 'default-avatar.png';
  selectedFile: File | null = null;

  constructor(private router: Router, private http: HttpClient, private datePipe: DatePipe) {}

  ngOnInit(): void {
    this.fetchProfile();
  }

  fetchProfile() {
    const token = localStorage.getItem('access_token');
    if (token) {
      const headers = new HttpHeaders({
        'Authorization': `Bearer ${token}`
      });
  
      this.http.get('http://127.0.0.1:8000/music/api/profile/', { headers }).subscribe({
        next: (data: any) => {
          this.profile = data;
          this.username = data.user.username || ''; // Теперь извлекаем username из ответа API
          this.loadLikedTracksFromProfile();
          this.loadCreatedTracks(); // Загружаем созданные треки
        },
        error: err => {
          alert('Ошибка при загрузке профиля. Пожалуйста, войдите заново.');
          this.router.navigate(['']);
        }
      });
    } else {
      alert('Необходимо войти в систему.');
      this.router.navigate(['']);
    }
  }
  

  loadLikedTracksFromProfile() {
    if (this.profile && Array.isArray(this.profile.liked_tracks)) {
      this.likedTracks = this.profile.liked_tracks;
    }
  }

  mediaBaseUrl = 'http://127.0.0.1:8000'; // Обязательно добавь это в начало класса!

loadCreatedTracks() {
  const token = localStorage.getItem('access_token');
  const headers = new HttpHeaders({
    'Authorization': `Bearer ${token}`
  });

  this.http.get<any[]>('http://127.0.0.1:8000/music/api/profile/created_tracks/', { headers }).subscribe({
    next: (data) => {
      this.createdTracks = data.map(track => {
        if (track.image && track.image.startsWith('/media')) {
          track.image = this.mediaBaseUrl + track.image;
        }
        if (track.audio && track.audio.startsWith('/media')) {
          track.audio = this.mediaBaseUrl + track.audio;
        }
        return track;
      });
    },
    error: err => {
      console.error('Ошибка при загрузке созданных треков:', err);
    }
  });
}

  

  getUsernameFromToken(token: string): string {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.username || '';
    } catch (e) {
      return '';
    }
  }

  deleteTrack(trackId: number) {
    const token = localStorage.getItem('access_token');
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });

    this.http.delete(`http://127.0.0.1:8000/music/api/delete-track/${trackId}/`, { headers }).subscribe({
      next: () => {
        this.createdTracks = this.createdTracks.filter(track => track.id !== trackId); // Убираем удалённый трек из списка
      },
      error: err => {
        console.error('Ошибка при удалении трека:', err);
      }
    });
  }

  uploadAvatar() {
    if (!this.selectedFile) return;
    const token = localStorage.getItem('access_token');
    const formData = new FormData();
    formData.append('avatar', this.selectedFile);

    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });

    this.http.put('http://127.0.0.1:8000/music/api/profile/', formData, { headers }).subscribe({
      next: (data: any) => {
        this.profile = data;
        this.selectedFile = null;
      },
      error: err => {
        console.error('Ошибка при загрузке аватара:', err);
      }
    });
  }

  removeAvatar() {
    const token = localStorage.getItem('access_token');
    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });

    this.http.put('http://127.0.0.1:8000/music/api/profile/', { avatar: null }, { headers }).subscribe({
      next: (data: any) => {
        this.profile = data;
      },
      error: err => {
        console.error('Ошибка при удалении аватара:', err);
      }
    });
  }

  setDefaultAvatar() {
    this.profile.avatar = this.defaultAvatar;
  }

  unlikeTrack(trackId: number) {
    const token = localStorage.getItem('access_token');
    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });

    this.http.post(`http://127.0.0.1:8000/music/api/tracks/${trackId}/like/`, {}, { headers }).subscribe({
      next: () => {
        this.likedTracks = this.likedTracks.filter(t => t.id !== trackId);
      },
      error: err => {
        console.error('Ошибка при удалении лайка:', err);
      }
    });
  }

  formatDate(date: string) {
    return this.datePipe.transform(date, 'medium') || '';
  }
  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
    }
  }


  triggerFileInput() {
    const fileInput = document.querySelector<HTMLInputElement>('input[type="file"]');
    fileInput?.click();
  }
  
}
