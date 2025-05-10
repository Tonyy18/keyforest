import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { ButtonModule } from 'primeng/button';
import { DialogService, DynamicDialogRef } from 'primeng/dynamicdialog';
import { CreateOrganizationDialogComponent } from '../../shared/create-organization-dialog/create-organization-dialog.component';
import { DialogFooterComponent } from '../../shared/dialog-templates/dialog-footer/dialog-footer.component';
import { AuthService } from '../../services/auth.service';
import { Organization } from '../../types/organization.type';

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

  constructor(
    public dialogService: DialogService,
    private translate: TranslateService,
    private router: Router,
    private authService: AuthService
  ) {
    if(authService.user!.connections.length > 0) {
      this.router.navigate(["/dashboard"]);
    }
  }

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

    this.ref.onClose.subscribe((organization: Organization) => {
      if (organization) {
        this.router.navigate(["/dashboard"])
      }
    });
  }

  ngOnDestroy() {
    if (this.ref) {
        this.ref.close();
    }
  }

}
