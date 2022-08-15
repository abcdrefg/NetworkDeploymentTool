import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DeviceService {
  backendServerAddress = 'http://127.0.0.1:5000';

  constructor(private httpClient: HttpClient) {}

  trySavingDevice(deviceWrapper: DeviceInfoWrapper) {
    return this.httpClient.post(
      this.backendServerAddress + '/deviceController/addDevice',
      deviceWrapper
    );
  }

  getDevices(devices: Array<string>) {
    return this.httpClient.post(
      this.backendServerAddress + '/deviceController/getRunningConfigs',
      devices)
  }
}

export interface DeviceInfoWrapper {
  username: string;
  password: string;
  secret: string;
  host: string;
  deviceType: string;
  name: string;
}
