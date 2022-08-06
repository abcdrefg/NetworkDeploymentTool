import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, Observable } from 'rxjs';
import { LoginCredentials } from './app.component';

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  backendServerAddress = 'http://127.0.0.1:5000';
  constructor(private httpClient: HttpClient) {}

  authenticate(
    login: String,
    password: String
  ): Observable<LoginAuthenticated> {
    const loginCredentials: LoginCredentials = {
      login: login,
      password: password,
    };
    return this.httpClient.post<LoginAuthenticated>(
      this.backendServerAddress + '/loginService/authenticate',
      loginCredentials
    );
  }

  checkToken(token: String): Observable<LoginAuthenticated> {
    return this.httpClient.post<LoginAuthenticated>(
      this.backendServerAddress + '/loginService/checkToken',
      token
    );
  }
}

export interface LoginAuthenticated {
  login: string;
  token: string;
}