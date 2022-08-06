import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { CookieService } from 'ngx-cookie-service';
import { MainComponent } from './main/main.component';
import { LandingComponent } from './landing/landing.component';
import { AuthService } from './auth.service';
import { AccountComponent } from './account/account.component';
import { AuthGuard } from './auth.guard';
import { AccountService } from './account.service';
import { DevicesPageComponent } from './devices-page/devices-page.component';
@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    MainComponent,
    LandingComponent,
    AccountComponent,
    DevicesPageComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [CookieService, AuthService, AuthGuard, AccountService],
  bootstrap: [AppComponent]
})
export class AppModule { }