import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { DeploymentService } from '../deployment.service';

@Component({
  selector: 'app-unit-test',
  templateUrl: './unit-test.component.html',
  styleUrls: ['./unit-test.component.css']
})
export class UnitTestComponent implements OnInit {
  @Output() updateStatus = new EventEmitter();
  showTestsPassed: boolean = false;
  showTestsFailed: boolean = false;
  isTestsRunning: boolean = false;
  errors: any;
  constructor(private deploymentService: DeploymentService) { }

  ngOnInit(): void {
    this.showTestsPassed = true;
  }

  finishStep(): void {
    this.deploymentService.finishUnitTest().subscribe((response) => {
      this.updateStatus.emit();
    })
  }

  runUnitTests(): void {

  }


}
