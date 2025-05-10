import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RadioButtonModule } from 'primeng/radiobutton';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { ButtonModule } from 'primeng/button';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { DialogFooterComponent } from '../../shared/dialog-templates/dialog-footer/dialog-footer.component';
import { CreateOrganizationDialogComponent } from '../../shared/create-organization-dialog/create-organization-dialog.component';
import { DialogService, DynamicDialogRef } from 'primeng/dynamicdialog';
import { BaseComponent } from '../../shared/base.component';
import { DashboardService } from '../../services/dashboard.service';
import { Organization } from '../../types/organization.type';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-organizations',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    RadioButtonModule,
    ButtonModule,
    TranslateModule
  ],
  templateUrl: './organizations.component.html',
  styleUrl: './organizations.component.scss'
})
export class OrganizationsComponent extends BaseComponent {

  protected authService: AuthService = inject(AuthService);
  protected dialogService: DialogService = inject(DialogService);
  protected dashboardService: DashboardService = inject(DashboardService);
  protected activatedRoute: ActivatedRoute = inject(ActivatedRoute);
  protected selected: number | undefined;
  ref: DynamicDialogRef | undefined;

  ngOnInit(): void {
    this.selected = this.dashboardService.activeOrganization?.id;
  }

  create(): void {
    this.ref = this.dialogService.open(CreateOrganizationDialogComponent, {
      header: this.translateService.instant('create_organization'),
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

  setActive() {
    if(this.selected != undefined) {
      const org = this.authService.user!.connections.filter(c => c.organization.id == this.selected)[0].organization;
      this.dashboardService.setActive(org);
      this.messagingService.add({
        severity: "success",
        summary: "organization_changed",
        detail: "active_organization_changed",
        detailMapping: {
          organization: org.name
        }
      })
      this.router.navigate(['roles'], {relativeTo: this.activatedRoute})
    }
  }

}
