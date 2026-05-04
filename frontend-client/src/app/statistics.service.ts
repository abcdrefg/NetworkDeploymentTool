import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class StatisticsService {

  backendServerAddress = 'http://127.0.0.1:5000';
  endpoint = '/statisticsService';
  constructor(private httpClient: HttpClient) {}

  getNumberOfDevices(): Observable<string> {
    return this.httpClient.get<string>(
      this.backendServerAddress + this.endpoint + '/getNumberOfDevices'
    );
  }

  getNumberOfUnitTests(): Observable<string> {
    return this.httpClient.get<string>(
      this.backendServerAddress + this.endpoint + '/getNumberOfUnitTests'
    );
  }

  getLastDeploy(): Observable<string> {
    return this.httpClient.get<string>(
      this.backendServerAddress + this.endpoint + '/getLastDeploy'
    );
  }
}
