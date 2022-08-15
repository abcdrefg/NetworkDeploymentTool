import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AccountComponent } from './account/account.component';
import { AuthGuard } from './auth.guard';
import { LandingComponent } from './landing/landing.component';
import { LoginComponent } from './login/login.component';
import { DevicesPageComponent } from './devices-page/devices-page.component';
const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'landing', component: LandingComponent, canActivate: [AuthGuard] },
  { path: '', redirectTo: '/landing', pathMatch: 'full' },
  { path: 'account', component: AccountComponent, canActivate: [AuthGuard] },
  { path: 'devices', component: DevicesPageComponent, canActivate: [AuthGuard]}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
