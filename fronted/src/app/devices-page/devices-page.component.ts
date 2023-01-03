import { Component, OnInit } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import {NgbModal, NgbModalOptions, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';
import { Observable } from 'rxjs';
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
  deviceType: string = 'router';
  deviceName: string = '';
  currentConfig: string = '';
  deviceConfigs: RunningConfig[] = [];
  isLoading: boolean = false;
  showSuccess = false;
  showError = false;
  isFetchingDevices: boolean = false;

  currentUsername: string = '';
  currentPassword: string = '';
  currentHost: string = '';
  currentSecret: string = '';
  currentDeviceType: string = '';
  currentName: string = '';

  constructor(private modalService: NgbModal, private deviceService: DeviceService) { 
    this.modalOptions = {
      backdrop:'static',
      backdropClass:'customBackdrop'
    }
  }

  ngOnInit(): void {
    this.getRunningConfigs();
  }

  open(content: any) {
    this.modalService.open(content, this.modalOptions).result.then((result) => {
      this.closeResult = `Closed with: ${result}`;
    }, (reason) => {
      this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;
    });
  }

  showConfig(name: string) {
    const configWrapper = this.deviceConfigs.filter((device) => {
      return device.name == name;
    })[0];
    this.currentConfig = configWrapper.config;
    this.currentHost = configWrapper.host;
    this.currentName = configWrapper.name;
    this.currentDeviceType = configWrapper.deviceType;
    this.currentPassword = configWrapper.password;
    this.currentSecret = configWrapper.secret;
    this.currentUsername = configWrapper.username;
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
        this.getRunningConfigs();
      },
      (error) => {console.log(error)
        this.isLoading = false;
        this.modalService.dismissAll();
        this.showError = true;
      });
  }

  getRunningConfigs() {
    this.isFetchingDevices = true;
    this.deviceService.getDevices().subscribe(
      (deviceConfigsData) => {
        this.deviceConfigs = deviceConfigsData;
        this.isFetchingDevices = false;
      },
      (error) => {
        console.log("ERORR", error);
        this.isFetchingDevices = false;
      }
    )
  } 
}

export interface RunningConfig {
  config: string;
  username: string;
  password: string;
  secret: string;
  host: string;
  deviceType: string;
  name: string;
}
