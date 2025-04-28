import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { ButtonModule } from 'primeng/button';
import { DialogService, DynamicDialogRef } from 'primeng/dynamicdialog';
import { LoginComponent } from '../login/login.component';
import { CreateOrganizationDialogComponent } from '../../shared/create-organization-dialog/create-organization-dialog.component';

@Component({
    selector: 'app-start-organization',
    imports: [
      ButtonModule,
      TranslateModule,
      RouterLink
    ],
    templateUrl: './start-organization.component.html',
    styleUrl: './start-organization.component.scss'
})
export class StartOrganizationComponent {

  ref: DynamicDialogRef | undefined;

  constructor(public dialogService: DialogService) {}

  create(): void {
    this.ref = this.dialogService.open(CreateOrganizationDialogComponent, {
      header: 'Select a Product',
      modal: true,
      closable: true,
    });
  }

}
