import { Component } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';

@Component({
    selector: 'app-create-organization-dialog',
    imports: [
      ButtonModule,
      TranslateModule,
      InputTextModule
    ],
    templateUrl: './create-organization-dialog.component.html',
    styleUrl: './create-organization-dialog.component.scss'
})
export class CreateOrganizationDialogComponent {
}
