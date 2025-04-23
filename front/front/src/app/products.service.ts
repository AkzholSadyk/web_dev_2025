import { Injectable } from '@angular/core';
import { AuthModel, Token } from '../models';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/internal/Observable';

@Injectable({
  providedIn: 'root'
})
export class ProductsService {

  constructor(private client: HttpClient) { }

  login(authModel: AuthModel): Observable<Token> {
    return this.client.post<Token>('http://127.0.0.1:8000/music/api/token/', authModel)
  }

  register(authModel: AuthModel): Observable<any> {
    return this.client.post('http://127.0.0.1:8000/music/api/register/', authModel);
  }
  
}
