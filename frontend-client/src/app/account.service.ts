import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CookieService } from 'ngx-cookie-service';
@Injectable({
  providedIn: 'root'
})
export class AccountService {
  backendServerAddress = 'http://127.0.0.1:5000';
  constructor(private httpClient: HttpClient, private cookieService: CookieService) { }

  changePassword(newPassword: string, oldPassword: string): Observable<boolean> {
    const passwords: PasswordsWrapper = {
      oldPassword: oldPassword,
      newPassword: newPassword,
      token: this.cookieService.get('Token')
    };
    return this.httpClient.post<boolean>(this.backendServerAddress + '/accountService/changePassword',
    passwords);
  }
}

export interface PasswordsWrapper {
  oldPassword: String;
  newPassword: String;
  token: String;
}
