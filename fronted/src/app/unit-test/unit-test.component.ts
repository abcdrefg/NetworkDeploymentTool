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
  results: any;

  constructor(private deploymentService: DeploymentService) { }

  ngOnInit(): void {}

  finishStep(): void {
    this.deploymentService.finishUnitTest().subscribe((response) => {
      this.updateStatus.emit();
    })
  }

  runUnitTests(): void {
    this.isTestsRunning = true;
    this.showTestsFailed = false;
    this.showTestsPassed = false;
    this.results = [];
    this.deploymentService.runTests().subscribe((results) => {
      this.results = results;
      this.isTestsRunning = false;
      if (results.length == 0) {
        this.showTestsPassed = true;
        return;
      }
      results = results.filter((res:any) => {
        return res.result != 'passed';
      });
      console.log(results);
      if (results.length != 0) {
        this.showTestsFailed = true;
      } else {
        this.showTestsPassed = true;
      }
    }, (err) => {
      console.log(err);
      this.isTestsRunning = false;
    })
  }


}
