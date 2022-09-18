import { Component, OnInit,EventEmitter ,ViewEncapsulation, Output } from '@angular/core';
import { DeploymentService } from '../deployment.service';

@Component({
  selector: 'app-deploy-tab',
  templateUrl: './deploy-tab.component.html',
  styleUrls: ['./deploy-tab.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class DeployTabComponent implements OnInit {
  @Output() updateStatus = new EventEmitter();
  error: string = '';
  deploymentFinished: boolean = false;
  deploymentFailed: boolean = false;
  isDeploymentRunning: boolean = false;
  isDeployed: boolean = false;
  diffrences: any;
  constructor(private deploymentService: DeploymentService) { }

  ngOnInit(): void {
    this.checkDeployStatus();
  }

  startDeployment(): void {
    this.isDeploymentRunning = true;
    this.deploymentFailed = false;
    this.deploymentFinished = false;
    this.deploymentService.deployConfigurations().subscribe((res) => {
      this.deploymentFinished = true;
      this.getDiffrences();
    }, (error) => {
      this.error = error['error']['errors'];
      this.deploymentFailed = true;
      this.isDeploymentRunning = false;
    })
  }

  getDiffrences(): void {
    this.deploymentService.getDiffrences().subscribe((diff) => {
      let listOfConfs = []
      for (const conf in diff) {
        listOfConfs.push({name: conf, diff: diff[conf]});
        
      }
      this.diffrences = listOfConfs;
      this.isDeploymentRunning = false;
      this.deploymentService.commit().subscribe((succ) => {}, (error) => {console.log(error)});
    }, (error) => {
      console.log(error);
      this.isDeploymentRunning = false;
    });
  }

  createNewDeploymentProcess(): void {
    this.deploymentService.startNewDeploymentProcess().subscribe((succ) => {
      this.checkDeployStatus();
      this.updateStatus.emit();
    }, (err) => {});
  }

  checkDeployStatus(): void {
    this.deploymentService.checkIsDeployed().subscribe((isDeployedStatus) => {
      this.isDeployed = true;
    }, (error) => {
      this.isDeployed = false;
    });
  }

}
