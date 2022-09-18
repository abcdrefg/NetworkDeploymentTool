import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

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
import { DeviceService } from './device.service';
import { ConfigurationPageComponent } from './configuration-page/configuration-page.component';
import { ConfigurationService } from './configuration.service';
import { DeploymentPageComponent } from './deployment-page/deployment-page.component';
import { ConfigurationTestComponent } from './configuration-test/configuration-test.component';
import { DeploymentService } from './deployment.service';
import { UnitTestComponent } from './unit-test/unit-test.component';
import { DeployTabComponent } from './deploy-tab/deploy-tab.component';
import { HistoryPageComponent } from './history-page/history-page.component';
import { UnitTestsPageComponent } from './unit-tests-page/unit-tests-page.component';
import { VersionControlService } from './version-control.service';
import { UnitTestManagementService } from './unit-test-management.service';
@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    MainComponent,
    LandingComponent,
    AccountComponent,
    DevicesPageComponent,
    ConfigurationPageComponent,
    DeploymentPageComponent,
    ConfigurationTestComponent,
    UnitTestComponent,
    DeployTabComponent,
    HistoryPageComponent,
    UnitTestsPageComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    NgbModule
  ],
  providers: [CookieService, AuthService, AuthGuard, AccountService, DeviceService, ConfigurationService, DeploymentService, VersionControlService, UnitTestManagementService],
  bootstrap: [AppComponent]
})
export class AppModule { }
