import { Component } from '@angular/core';
import { AuthModel, Token } from '../../models';
import { ProductsService } from '../products.service';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';


@Component({
  selector: 'app-home',
  standalone: true,
  imports: [FormsModule,RouterModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  authModel: AuthModel;
  
  constructor(private productsService: ProductsService,private router: Router){
    this.authModel = {} as AuthModel
  }

  login() {
    this.productsService.login(this.authModel).subscribe((token: Token) => {
      console.log('Получен токен:', token);  // Логируем токен для проверки
      localStorage.setItem('access_token', token.access);  // Сохраняем токен в localStorage
      localStorage.setItem('refresh_token', token.refresh);  // Можно также сохранить refresh токен
      this.router.navigate(['/main']);
    }, error => {
      console.error('Ошибка при логине:', error);  // Логируем ошибку, если она произошла
    });
  }
  
  register() {
    this.productsService.register(this.authModel).subscribe({
      next: () => {
        alert('Успешная регистрация!');
      },
      error: (err) => {
        alert('Ошибка регистрации!');
        console.error(err);
      }
    });
  }
  
}
