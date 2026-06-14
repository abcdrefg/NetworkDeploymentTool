import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UnitTestManagementService {
  backendServerAddress = 'http://127.0.0.1:5000';

  constructor(private httpClient: HttpClient) {}

  insertTest(file: any, filename: string): Observable<any> {
    const fileWrapper = {
      "file": file,
      "filename": filename
    }
    return this.httpClient.post<any>(this.backendServerAddress + '/unitTestController/insertTest', fileWrapper);
  }

  activateTest(testname: string): Observable<any> {
    return this.httpClient.post<any>(this.backendServerAddress + '/unitTestController/activateTest', {"testname": testname})
  }

  disableTest(testname: string): Observable<any> {
    return this.httpClient.post<any>(this.backendServerAddress + '/unitTestController/disableTest', {"testname": testname})
  }

  getTests(): Observable<any> {
    return this.httpClient.get<any>(this.backendServerAddress + '/unitTestController/getTests')
  }
}
