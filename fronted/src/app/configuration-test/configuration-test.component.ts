import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { DeploymentService } from '../deployment.service';
import { NgbAccordion } from '@ng-bootstrap/ng-bootstrap';
@Component({
  selector: 'app-configuration-test',
  templateUrl: './configuration-test.component.html',
  styleUrls: ['./configuration-test.component.css']
})

export class ConfigurationTestComponent implements OnInit {
  @Output() updateStatus = new EventEmitter();
  isTestsRunning: boolean = false;
  errors: ErrorsMap[] = [];
  showTestsPassed: boolean = false;
  showTestsFailed: boolean = false;
  constructor(private deploymentServie: DeploymentService) { }

  ngOnInit(): void {
  }

  testConfigs(): void {
    this.isTestsRunning = true;
    this.deploymentServie.testConfigs().subscribe((response) => {
      this.errors = response;
      this.isTestsRunning = false;
      if (this.errors.length == 0) {
        this.showTestsPassed = true;
      } else {
        this.showTestsFailed = true;
      }
    }, (err) => {
      console.log(err);
      this.isTestsRunning = false;
    })
  }

  finishStep(): void {
    this.deploymentServie.finishSyntaxTest().subscribe((finish) => {
      this.updateStatus.emit();
    })
  }

}

export interface ErrorsMap {
  device: string,
  errors: string
}