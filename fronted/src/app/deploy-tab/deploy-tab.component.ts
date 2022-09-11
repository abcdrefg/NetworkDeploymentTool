import { Component, OnInit } from '@angular/core';
import { DeploymentService } from '../deployment.service';

@Component({
  selector: 'app-deploy-tab',
  templateUrl: './deploy-tab.component.html',
  styleUrls: ['./deploy-tab.component.css']
})
export class DeployTabComponent implements OnInit {
  error: string = '';
  deploymentFinished: boolean = false;
  deploymentFailed: boolean = false;
  isDeploymentRunning: boolean = false;
  constructor(private deploymentService: DeploymentService) { }

  ngOnInit(): void {
  }

  startDeployment(): void {
    this.isDeploymentRunning = true;
    this.deploymentFailed = false;
    this.deploymentFinished = false;
    this.deploymentService.deployConfigurations().subscribe((res) => {
      this.deploymentFinished = true;
      
      this.isDeploymentRunning = false;
    }, (error) => {
      this.error = error['error']['errors'];
      this.deploymentFailed = true;
      this.isDeploymentRunning = false;
    })
  }

}
