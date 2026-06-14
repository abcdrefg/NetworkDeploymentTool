import { Component, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { LoginService } from '../login.service';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';
@Component({
  selector: 'app-login-component',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {
  constructor(
    private loginService: LoginService,
    private cookieService: CookieService,
    private authService: AuthService,
    private router: Router
  ) {}
  login: String = '';
  password: String = '';
  token: String = '';
  user: String = '';
  ngOnInit(): void {}

  onLogin() {
    this.loginService.authenticate(this.login, this.password).subscribe(
      (loginAuth) => {
        this.authService.login(loginAuth.token);
        this.router.navigate(['landing']);
      },
      (error) => console.log(error)
    );
  }
}
