import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class VersionControlService {
  backendServerAddress = 'http://127.0.0.1:5000';

  constructor(private httpClient: HttpClient) {}

  getHistoricalVersionDiff(id: string): Observable<any> {
    const versionId = {"Id": id};
    return this.httpClient.post<any>(
      this.backendServerAddress + '/versionController/getHistoricalVersionDiff', versionId);
  }

  fetchVersions(): Observable<any> {
    return this.httpClient.get<any>(
      this.backendServerAddress + '/versionController/getVersions');
  }

  rollbackToId(id: string): Observable<any> {
    const versionId = {"Id": id};
    return this.httpClient.post<any>(
      this.backendServerAddress + '/versionController/rollbackToId', versionId);
  
  }
}
