import { Component, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { LoginService } from '../login.service';

@Component({
  selector: 'app-login-component',
  templateUrl: './login-component.component.html',
  styleUrls: ['./login-component.component.css']
})
export class LoginComponentComponent implements OnInit {

  constructor(private loginService : LoginService, private cookieService: CookieService) { }
  login: String = '';
  password: String = '';
  token: String = '';
  user: String = '';
  ngOnInit(): void {}

  onLogin() {
    this.loginService.authenticate(this.login, this.password).subscribe((loginAuth) => {
      this.cookieService.set('Token', loginAuth.token)
      console.log(this.cookieService.get('Token'));
    }, (error) => console.log(error));
  }
}
