import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-create-track',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './create-track.component.html',
  styleUrls: ['./create-track.component.css']
})
export class CreateTrackComponent {
  createTrackForm: FormGroup;

  constructor(private fb: FormBuilder, private http: HttpClient, private router: Router) {
    this.createTrackForm = this.fb.group({
      title: [''],
      artist: [''],
      album: [''],
      image: [null],
      audio: [null]
    });
  }

  onSubmit() {
    console.log('[CreateTrackComponent] Попытка создать трек...');
  
    const formData = new FormData();
    formData.append('title', this.createTrackForm.get('title')?.value);
    formData.append('artist', this.createTrackForm.get('artist')?.value);
    formData.append('album', this.createTrackForm.get('album')?.value);
    formData.append('image', this.createTrackForm.get('image')?.value);
    formData.append('audio', this.createTrackForm.get('audio')?.value);
  
    const token = localStorage.getItem('access_token');
    console.log('[CreateTrackComponent] Токен из localStorage:', token);
  
    if (!token) {
      console.warn('[CreateTrackComponent] Токен не найден! Перенаправление на логин...');
      alert('Необходимо войти в систему для создания трека.');
      this.router.navigate(['']);
      return;
    }
  
    // Только заголовок для авторизации, без Content-Type
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  
    console.log('[CreateTrackComponent] Заголовки отправки:', headers);
  
    this.http.post('http://127.0.0.1:8000/music/api/create-tracks/', formData, { headers }).subscribe(
      response => {
        console.log('[CreateTrackComponent] Трек успешно создан:', response);
        this.router.navigate(['/tracks']);
      },
      error => {
        console.error('[CreateTrackComponent] Ошибка при создании трека:', error);
        alert('Произошла ошибка при создании трека.');
      }
    );
  }
  

  onFileChange(event: any, field: string) {
    const file = event.target.files[0];
    if (file) {
      this.createTrackForm.patchValue({ [field]: file });
    }
  }
}
