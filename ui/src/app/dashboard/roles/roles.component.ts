import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { BaseComponent } from '../../shared/base.component';
import { TagModule } from 'primeng/tag';
import { PermissionService } from '../../services/permission.service';
import { Permission } from '../../types/permission.type';
import { DialogFooterComponent } from '../../shared/dialog-templates/dialog-footer/dialog-footer.component';
import { CreateRoleDialogComponent } from '../../shared/create-role-dialog/create-role-dialog.component';
import { DialogService, DynamicDialogRef } from 'primeng/dynamicdialog';

@Component({
  selector: 'app-roles',
  imports: [
    CommonModule,
    ButtonModule,
    TranslateModule,
    TagModule
  ],
  templateUrl: './roles.component.html',
  styleUrl: './roles.component.scss'
})
export class RolesComponent extends BaseComponent {

  ref: DynamicDialogRef | undefined;
  dialogService: DialogService = inject(DialogService);

  create(): void {
    this.ref = this.dialogService.open(CreateRoleDialogComponent, {
      header: this.translateService.instant('create_role'),
      modal: true,
      closable: true,
      width: '520px',
      breakpoints: {
        '530px': '95vw',
      },
      templates: {
        footer: DialogFooterComponent
      }
    });
    
    this.ref.onClose.subscribe(() => {

    });
  }
}
