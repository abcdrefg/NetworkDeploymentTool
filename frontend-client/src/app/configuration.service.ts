import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { DeviceCommands } from './configuration-page/configuration-page.component';

@Injectable({
  providedIn: 'root'
})
export class ConfigurationService {

  backendServerAddress = 'http://127.0.0.1:5000';

  constructor(private httpClient: HttpClient) { }

  getCommands(): Observable<DeviceCommands[]> {
    return this.httpClient.get<DeviceCommands[]>(
      this.backendServerAddress + '/configurationController/getCommands')
  }

  upsertCommands(deviceCommands: DeviceCommands[]) {
    return this.httpClient.put<DeviceCommands[]>(
      this.backendServerAddress + '/configurationController/upsertCommands', deviceCommands);
  }

  checkIsEditEnabled(): Observable<any> {
    return this.httpClient.get<any>(
      this.backendServerAddress + '/configurationController/isEditEnabled');
  }
}
