import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { ButtonModule } from 'primeng/button';
import { DynamicDialogConfig, DynamicDialogRef } from 'primeng/dynamicdialog';

@Component({
    selector: 'app-dialog-footer.component',
    imports: [
      ButtonModule,
      TranslateModule
    ],
    templateUrl: './dialog-footer.component.html',
    styleUrl: './dialog-footer.component.scss'
})
export class DialogFooterComponent {
  constructor(public ref: DynamicDialogRef, public config: DynamicDialogConfig) {

  }
}
