import { Component, OnInit } from '@angular/core';
import { UnitTestManagementService } from '../unit-test-management.service';

@Component({
  selector: 'app-unit-tests-page',
  templateUrl: './unit-tests-page.component.html',
  styleUrls: ['./unit-tests-page.component.css']
})
export class UnitTestsPageComponent implements OnInit {

  dataFetching: boolean = false;
  testsList: any;

  constructor(private unitTestMgt: UnitTestManagementService) { }

  ngOnInit(): void {
    this.reloadPage();
  }

  activateTest(testname: string): void {
    this.unitTestMgt.activateTest(testname).subscribe((succ) => {
      this.reloadPage();
    }, (err) => {
      console.log(err);
    });
  }

  disableTest(testname: string): void {
    this.unitTestMgt.disableTest(testname).subscribe((succ) => {
      this.reloadPage();
    }, (err) => {
      console.log(err);
    });
  }

  addTest(event: any): void {
    let file: File = event.target.files[0];
    console.log()
    let fileReader = new FileReader();
    fileReader.onload = (e) => {
      console.log(fileReader.result);
      this.unitTestMgt.insertTest(fileReader.result, file.name).subscribe((succ) => {
        this.reloadPage();
      }, (err) => {
        console.log(err);
      })
    }
    fileReader.readAsText(file);
  }

  private reloadPage(): void {
    this.dataFetching = true;
    this.unitTestMgt.getTests().subscribe((tests) => {
      this.testsList = tests;
      this.dataFetching = false;
    }, (err) => {
      console.log(err);
      this.dataFetching = false;
    })
  }

}
