import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ErrorsMap } from './configuration-test/configuration-test.component';
import { HttpClient } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class DeploymentService {

  backendServerAddress = 'http://127.0.0.1:5000';

  constructor(private httpClient: HttpClient) { }

  testConfigs(): Observable<ErrorsMap[]> {
    return this.httpClient.get<ErrorsMap[]>(
      this.backendServerAddress + '/deploymentController/testConfigs');
  }

  getStatus(): Observable<any> {
    return this.httpClient.get<any>(
      this.backendServerAddress + '/deploymentController/getStatus');
  }

  finishSyntaxTest(): Observable<any> {
    return this.httpClient.head(
      this.backendServerAddress + '/deploymentController/finishSyntaxTest');
  }

  finishUnitTest(): Observable<any> {
    return this.httpClient.head(
      this.backendServerAddress + '/deploymentController/finishUnitTest');
  }

  deployConfigurations(): Observable<any> {
    return this.httpClient.get(
      this.backendServerAddress + '/deploymentController/deployConfigurations');
  }

  getDiffrences(): Observable<any> {
    return this.httpClient.get<any>(
      this.backendServerAddress + '/deploymentController/getDiffrences');
  }

  commit(): Observable<any> {
    return this.httpClient.head(
      this.backendServerAddress + '/deploymentController/createSnapshot');  
  }

  checkIsDeployed(): Observable<any> {
    return this.httpClient.get<any>(
      this.backendServerAddress + '/deploymentController/checkDeploy');
  }

  startNewDeploymentProcess(): Observable<any> {
    return this.httpClient.head<any>(
      this.backendServerAddress + '/deploymentController/startNewProcess');
  }

  terminateProccess(): Observable<any> {
    return this.httpClient.head<any>(
      this.backendServerAddress + '/deploymentController/terminateProcess');
  }

  runTests(): Observable<any> {
    return this.httpClient.get<any>(
      this.backendServerAddress + '/deploymentController/runTests');
  }
}
