import { Component, OnInit } from '@angular/core';
import { DeploymentService } from '../deployment.service';

@Component({
  selector: 'app-deployment-page',
  templateUrl: './deployment-page.component.html',
  styleUrls: ['./deployment-page.component.css']
})
export class DeploymentPageComponent implements OnInit {
  progressBar: number = 25;
  activeStep: string = 'display-6';
  unactiveStep: string = 'text-muted';
  configTestsClass: string = 'text-muted';
  deployClass: string = 'text-muted';
  unitTestsClass: string = 'text-muted';
  deployStatus: string = '';
  constructor(private deploymentService: DeploymentService) {
    this.updateStatus();
  }

  ngOnInit(): void {
  }

  updateStatus(): void {
    this.deploymentService.getStatus().subscribe((response) => {
      let status = response['DeployStatus'];
      this.deployStatus = status;
      if (status == 'SyntaxTest') {
        this.configTestsClass = this.activeStep;
        this.deployClass = this.unactiveStep;
        this.unitTestsClass = this.unactiveStep;
      }
      if (status == 'UnitTest') {
        this.configTestsClass = this.unactiveStep;
        this.deployClass = this.unactiveStep;
        this.unitTestsClass = this.activeStep;
      }
      if (status == 'Deployment') {
        this.configTestsClass = this.unactiveStep;
        this.deployClass = this.activeStep;
        this.unitTestsClass = this.unactiveStep;
      }
    })
  }
}
