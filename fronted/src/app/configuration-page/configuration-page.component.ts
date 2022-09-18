import { Component, OnInit } from '@angular/core';
import { ConfigurationService } from '../configuration.service';
import { DeviceService } from '../device.service';
import { RunningConfig } from '../devices-page/devices-page.component';

@Component({
  selector: 'app-configuration-page',
  templateUrl: './configuration-page.component.html',
  styleUrls: ['./configuration-page.component.css']
})
export class ConfigurationPageComponent implements OnInit {

  isFetchingDevices: boolean = false;
  deviceConfigs: RunningConfig[] = [];
  deviceCommands: DeviceCommands[] = [];
  config: string = '';
  configCopy: string = '';
  editMode: boolean = false;
  currentDevice: string = '';
  isEditEnabled: boolean = false;
  constructor(private deviceService: DeviceService, private configurationService: ConfigurationService) {
    this.getCommands();
    this.getRunningConfigs();
  }

  ngOnInit(): void {
    this.configurationService.checkIsEditEnabled().subscribe((succ) => {
      this.isEditEnabled = true;
    }, (err) => {
      this.isEditEnabled = false;
    })
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

  unlockEdit() {
    this.editMode = true;
    this.configCopy = this.config;
  }

  cancelEdit() {
    if (this.editMode == false) {
      return;
    }
    this.editMode = false;
    this.config = this.configCopy;
  }

  saveEdit() {
    if (this.editMode == false) {
      return;
    }
    this.editMode = false;
    if (this.deviceCommands == null) {
      this.deviceCommands = [{
        name: this.currentDevice,
        commands: this.config
      }];
    }
    if (this.deviceCommands.filter((device) => {
      return device.name == this.currentDevice;
    }).length == 0) {
      this.deviceCommands.push({
        name: this.currentDevice,
        commands: this.config
      });
    } else {
      this.deviceCommands.filter((device) => {
        return device.name == this.currentDevice;
      })[0].commands = this.config;
    }
    this.configurationService.upsertCommands(this.deviceCommands).subscribe(
      (succ) => {
        this.getCommands();
      },
      (error) => {
        console.log("ERORR", error);
      }
    )
  }

  getCommands() {
    this.configurationService.getCommands().subscribe(
      (deviceCommandsData) => {
        this.deviceCommands = deviceCommandsData;
        console.log(this.deviceCommands);
      },
      (error) => {
        console.log("ERORR", error);
      }
    )
  }

  showConfig(name:string) {
    this.currentDevice = name;
    if (this.deviceCommands == null) {
      this.config = '';
    }
    this.config = this.deviceCommands.filter((device) => {
      return device.name == name;
    })[0]?.commands;
    if (this.config == null) {
      this.config = '';
    }
  }
}

export interface DeviceCommands {
  name: string,
  commands: string
}
