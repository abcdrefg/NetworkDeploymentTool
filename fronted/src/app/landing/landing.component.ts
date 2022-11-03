import { Component, OnInit } from '@angular/core';
import { StatisticsService } from '../statistics.service';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css']
})
export class LandingComponent implements OnInit {
  devices: string = '0';
  lastDeploy: string = 'Never';
  unitTests: string = '0';

  constructor(statisticsService: StatisticsService) { 
    statisticsService.getLastDeploy().subscribe(timestamp => {
      this.lastDeploy = timestamp;
    }, err => {
      console.log(err);
    });

    statisticsService.getNumberOfDevices().subscribe(devicesCount => {
      this.devices = devicesCount;
    }, err => {
      console.log(err);
    });

    statisticsService.getNumberOfUnitTests().subscribe(unitTestsCount => {
      this.unitTests = unitTestsCount;
    }, err => {
      console.log(err);
    });
  }

  ngOnInit(): void {
  }

}
