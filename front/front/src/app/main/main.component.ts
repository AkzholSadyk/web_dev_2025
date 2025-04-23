import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-main',
  standalone: true,
  imports: [CommonModule,FormsModule],
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {
  tracks: any[] = [];
  foundUsers: any[] = [];  // Исправлено: указали правильный тип
  searchQuery: string = '';
  defaultAvatar = 'default-avatar.png';
  constructor(private router: Router, private http: HttpClient) {}

  ngOnInit() {
    this.fetchTracks();
  }

  fetchTracks() {
    console.log('Checking token in localStorage...');
    const token = localStorage.getItem('access_token');
    console.log('Token from localStorage:', token);  // Выводим токен в консоль
  
    if (token) {
      console.log('Token found, making API request...');
      this.http.get<any[]>('http://127.0.0.1:8000/music/api/search/tracks/', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }).subscribe(
        data => {
          console.log('Tracks fetched successfully:', data);
          this.tracks = data;
        },
        error => {
          console.error('Error fetching tracks:', error);
          alert('Ошибка при загрузке треков.');
        }
      );
    } else {
      console.log('No token found in localStorage, redirecting to login...');
      alert('Необходимо войти в систему для доступа к данным.');
      this.router.navigate(['']);  // Перенаправить на страницу логина
    }
  }
  
  
  

  createTrack() {
    this.router.navigate(['/create-track']);
  }

  profile() {
    this.router.navigate(['/profile']);
  }

  logout() {
    this.router.navigate(['']);
  }


  likeTrack(trackId: number) {
    const token = localStorage.getItem('access_token');
  
    if (!token) {
      alert('Сначала войдите в систему!');
      this.router.navigate(['']);  // Перенаправление на логин
      return;
    }
  
    this.http.post(
      `http://127.0.0.1:8000/music/api/tracks/${trackId}/like/`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    ).subscribe({
      next: (response: any) => {
        const track = this.tracks.find(t => t.id === trackId);
        if (track) {
          track.like_count = response.like_count;
          // Можно добавить флаг "лайкнуто" при желании
        }
      },
      error: (err) => {
        console.error('Ошибка при лайке трека:', err);
        alert('Ошибка при лайке трека.');
      }
    });
  }


  searchUsers(searchQuery: string) {
    console.log('Checking token in localStorage...');
    const token = localStorage.getItem('access_token');
    console.log('Token from localStorage:', token);  // Выводим токен в консоль
  
    if (token) {
      console.log('Token found, making API request...');
      const url = `http://localhost:8000/music/api/search/users/?search=${searchQuery}`;
  
      this.http.get<any[]>(url, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }).subscribe(
        (response: any[]) => {
          console.log('Search results:', response);
          this.foundUsers = response;  // Сохраняем результаты поиска
        },
        (error) => {
          console.error('Search error:', error);
          alert('Ошибка при поиске пользователей.');
        }
      );
    } else {
      console.log('No token found in localStorage, redirecting to login...');
      alert('Необходимо войти в систему для доступа к данным.');
      this.router.navigate(['']);  // Перенаправить на страницу логина
    }
  }
  
  

  goToUserProfile(userId: number) {
    this.router.navigate(['/profile', userId]);  // Передаем userId в параметры маршрута
  }



  selectedTrack: any = null;

  openPlayer(track: any) {
    this.selectedTrack = track;
    this.isPlaying = false;
  
    // Ждём, пока Angular вставит DOM-элемент
    setTimeout(() => {
      const audio = document.querySelector('audio') as HTMLAudioElement;
  
      if (audio) {
        const playPromise = audio.play();
  
        if (playPromise !== undefined) {
          playPromise
            .then(() => {
              this.isPlaying = true;
              console.log('Автовоспроизведение пошло');
            })
            .catch((error) => {
              console.warn('Браузер заблокировал автозапуск, ждёт взаимодействия пользователя');
              // Можно показать подсказку типа "Нажми Play"
            });
        }
      }
    }, 100);
  }

closePlayer() {
  this.selectedTrack = null;
}

isPlaying = false;
progress = 0;
currentTime = '0:00';
duration = '0:00';

togglePlay(audio: HTMLAudioElement) {
  if (audio.paused) {
    audio.play();
    this.isPlaying = true;
  } else {
    audio.pause();
    this.isPlaying = false;
  }
}

updateProgress(audio: HTMLAudioElement) {
  this.progress = (audio.currentTime / audio.duration) * 100;
  this.currentTime = this.formatTime(audio.currentTime);
}

initDuration(audio: HTMLAudioElement) {
  this.duration = this.formatTime(audio.duration);
}

seek(event: MouseEvent, audio: HTMLAudioElement) {
  const container = event.currentTarget as HTMLElement;
  const rect = container.getBoundingClientRect();
  const offsetX = event.clientX - rect.left;
  const percent = offsetX / rect.width;
  audio.currentTime = percent * audio.duration;
  this.progress = percent * 100;
}

formatTime(time: number): string {
  const minutes = Math.floor(time / 60);
  const seconds = Math.floor(time % 60).toString().padStart(2, '0');
  return `${minutes}:${seconds}`;
}





}
