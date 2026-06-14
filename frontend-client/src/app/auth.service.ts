import { Injectable } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private token = '';
  constructor(private cookieService: CookieService) {}

  login(token: string) {
    this.cookieService.set('Token', token);
    this.token = token;
  }

  private checkToken(): boolean {
    if (this.cookieService.get('Token') != this.token) {
      return false;
    }
    if (this.token.length == 0) {
      return false;
    }
    return true;
  }

  logout() {
    this.cookieService.delete('Token');
    this.token = '';
  }

  checkIsLogged(): boolean {
    return this.checkToken();
  }
}
