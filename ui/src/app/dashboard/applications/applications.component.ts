import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { BaseComponent } from '../../shared/base.component';
import { DialogService, DynamicDialogRef } from 'primeng/dynamicdialog';
import { DialogFooterComponent } from '../../shared/dialog-templates/dialog-footer/dialog-footer.component';
import { CreateApplicationDialogComponent } from '../../shared/create-application-dialog/create-application-dialog.component';

@Component({
  selector: 'app-applications',
  imports: [
    CommonModule,
    ButtonModule,
    TranslateModule
  ],
  templateUrl: './applications.component.html',
  styleUrl: './applications.component.scss'
})
export class ApplicationsComponent extends BaseComponent {
  
  ref: DynamicDialogRef | undefined;
  dialogService: DialogService = inject(DialogService);

  create(): void {
    this.ref = this.dialogService.open(CreateApplicationDialogComponent, {
      header: this.translateService.instant('create_application'),
      modal: true,
      closable: true,
      width: '450px',
      breakpoints: {
        '460px': '95vw',
      },
      templates: {
        footer: DialogFooterComponent
      }
    });
    
    this.ref.onClose.subscribe(() => {

    });
  }

  ngOnDestroy() {
    if (this.ref) {
      this.ref.close();
    }
  }
}
