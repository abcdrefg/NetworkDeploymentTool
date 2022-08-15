import { Component, OnInit } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import {NgbModal, NgbModalOptions, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';
import { DeviceService } from '../device.service';
import { DeviceInfoWrapper } from '../device.service';
declare var window: any;
@Component({
  selector: 'app-devices-page',
  templateUrl: './devices-page.component.html',
  styleUrls: ['./devices-page.component.css']
})
export class DevicesPageComponent implements OnInit {

  hideComponent: Boolean = true;
  deviceAddModal: any;
  modalOptions: NgbModalOptions;
  closeResult: string = '';
  username: string = '';
  password: string = '';
  host: string = '';
  secret: string = '';
  deviceType: string = 'Router';
  deviceName: string = '';
  isLoading: boolean = false;
  showSuccess = false;
  showError = false;
  devices = ["FirstDevice", "SecondDevice"];
  constructor(private modalService: NgbModal, private deviceService: DeviceService) { 
    this.modalOptions = {
      backdrop:'static',
      backdropClass:'customBackdrop'
    }
  }

  ngOnInit(): void {
  }

  open(content: any) {
    this.modalService.open(content, this.modalOptions).result.then((result) => {
      this.closeResult = `Closed with: ${result}`;
    }, (reason) => {
      this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;
    });
  }

  private getDismissReason(reason: any): string {
    if (reason === ModalDismissReasons.ESC) {
      return 'by pressing ESC';
    } else if (reason === ModalDismissReasons.BACKDROP_CLICK) {
      return 'by clicking on a backdrop';
    } else {
      return  `with: ${reason}`;
    }
  }

  trySaveDevice():void {
    this.isLoading = true;
    const deviceWrapper: DeviceInfoWrapper = {
      username: this.username,
      password: this.password,
      host: this.host,
      secret: this.secret,
      deviceType: this.deviceType,
      name: this.deviceName
    }
    this.deviceService.trySavingDevice(deviceWrapper).subscribe(
      (deviceSaved) => {
        this.isLoading = false;
        this.modalService.dismissAll();
        this.showSuccess = true;
      },
      (error) => {console.log(error)
        this.isLoading = false;
        this.modalService.dismissAll();
        this.showError = true;
        this.getRunningConfigs(this.devices);
      });
  }

  getRunningConfigs(devices: Array<string>): void {
    this.deviceService.getDevices(devices).subscribe(
      (deviceConfigs) => {
        console.log(deviceConfigs);
      },
      (error) => {
        console.log("ERRRRRRRROOOORR", error);
      }
    )
  } 
}
