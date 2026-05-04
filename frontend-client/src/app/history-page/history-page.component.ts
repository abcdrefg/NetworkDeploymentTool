import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import {NgbModal, NgbModalOptions, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';
import { VersionControlService } from '../version-control.service';
@Component({
  selector: 'app-history-page',
  templateUrl: './history-page.component.html',
  styleUrls: ['./history-page.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class HistoryPageComponent implements OnInit {
  isLoading: boolean = false;
  modalOptions: NgbModalOptions;
  closeResult: string = '';
  versionDiff: any;
  versions: any;
  dataFetching: boolean = false;
  currentIdToRestore: string = '';
  timestampToRestore: string = '';
  isRestoring: boolean = false;
  restored: boolean = false;
  failed: boolean = false;

  constructor(private modalService: NgbModal, private versionControlService: VersionControlService) {
    this.modalOptions = {
      backdrop:'static',
      backdropClass:'customBackdrop',
      size: 'xl'
    }
  }

  ngOnInit(): void {
    this.versionControlService.fetchVersions().subscribe((versions) => {
      this.versions = versions;
    }, (err) => {
      console.log(err);
    })
  }

  tryOpen(id: string): void {
    this.isLoading = true;
    this.getVersionDiff(id);
  }

  open(content: any, id: string) {
    this.tryOpen(id);
    this.modalService.open(content, this.modalOptions).result.then((result) => {
      this.closeResult = `Closed with: ${result}`;
    }, (reason) => {
      this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;
    });
  }

  rollback() {
    this.isRestoring = true;
    this.restored = false;
    this.versionControlService.rollbackToId(this.currentIdToRestore).subscribe((succ) => {
      this.restored = true;
      this.isRestoring = false;
    }, (err) => {
      console.log(err);
      this.isRestoring = false;
    });
  }

  rollbackWindow(content: any, id:string, timestamp:string) {
    this.isRestoring = false;
    this.restored = false;
    this.failed = false;
    this.currentIdToRestore = id;
    this.timestampToRestore = timestamp;
    this.modalService.open(content, this.modalOptions).result.then((result) => {
      this.closeResult = `Closed with: ${result}`;
    }, (reason) => {
      this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;
    });
  }

  private getVersionDiff(id: string): void {
    this.versionDiff = null;
    this.versionControlService.getHistoricalVersionDiff(id).subscribe((diffrences) => {
      let listOfConfs = []
      for (const conf in diffrences) {
        listOfConfs.push({name: conf, diff: diffrences[conf]});
        
      }
      this.versionDiff = listOfConfs;
      this.isLoading = false;
    }, (err) => {
      console.log(err);
      this.isLoading = false;
    })
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

}
