import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { ButtonModule } from 'primeng/button';
import { DialogService, DynamicDialogRef } from 'primeng/dynamicdialog';
import { LoginComponent } from '../login/login.component';
import { CreateOrganizationDialogComponent } from '../../shared/create-organization-dialog/create-organization-dialog.component';
import { DialogFooterComponent } from '../../shared/dialog-templates/dialog-footer/dialog-footer.component';
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

  constructor(public dialogService: DialogService, private translate: TranslateService) {}

  create(): void {
    this.ref = this.dialogService.open(CreateOrganizationDialogComponent, {
      header: this.translate.instant('create_organization'),
      modal: true,
      closable: true,
      width: '450px',
      breakpoints: {
        '500px': '95vw',
      },
      templates: {
        footer: DialogFooterComponent
      }
    });
  }

  ngOnDestroy() {
    if (this.ref) {
        this.ref.close();
    }
  }

}
