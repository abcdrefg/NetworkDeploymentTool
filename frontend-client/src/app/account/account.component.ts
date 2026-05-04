import { Component, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { AccountService } from '../account.service';

@Component({
  selector: 'app-account',
  templateUrl: './account.component.html',
  styleUrls: ['./account.component.css']
})
export class AccountComponent implements OnInit {
  token: string = '';
  currentPassword: string = '';
  newPassword: string = '';
  newPasswordRepeated: string = '';
  constructor(private cookieService: CookieService, private accountService: AccountService) { }

  ngOnInit(): void {
    this.token =  this.cookieService.get('Token');
  }

  changePassword() {
    if (this.newPassword != this.newPasswordRepeated) {
      console.log('Hasła się różnią');
      return;
    }
    this.accountService.changePassword(this.newPassword, this.currentPassword).subscribe((success) => {
      console.log(success);
    }, (error) => {
      console.log(error);
    });
  }

}
