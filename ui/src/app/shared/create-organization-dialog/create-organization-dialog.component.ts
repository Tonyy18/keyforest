import { Component, inject } from '@angular/core';
import { FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { ButtonModule } from 'primeng/button';
import { DynamicDialogConfig, DynamicDialogRef } from 'primeng/dynamicdialog';
import { InputTextModule } from 'primeng/inputtext';
import { TextareaModule } from 'primeng/textarea';
import { BaseComponent } from '../base.component';
import { FormControlDirective } from '../../directives/form-control.directive';
import { Organization } from '../../types/organization.type';
import { OrganizationService } from '../../services/organization.service';
@Component({
    selector: 'app-create-organization-dialog',
    imports: [
      ButtonModule,
      TranslateModule,
      InputTextModule,
      TextareaModule,
      ReactiveFormsModule,
      FormControlDirective
    ],
    templateUrl: './create-organization-dialog.component.html',
    styleUrl: './create-organization-dialog.component.scss'
})
export class CreateOrganizationDialogComponent extends BaseComponent{

  public config: DynamicDialogConfig = inject(DynamicDialogConfig);
  private ref: DynamicDialogRef = inject(DynamicDialogRef);
  protected service: OrganizationService = inject(OrganizationService);
  
  frm: FormGroup = this.fb.group({
    name: [undefined, [Validators.required, Validators.minLength(3), Validators.maxLength(50)]],
    description: [undefined, Validators.maxLength(400)],
  })

  ngOnInit(): void {
    //For footer
    this.config.data ? this.config.data.save = () => {
      this.save();
    } : this.config.data = { save: () => { this.save(); } };
  }

  save(): void {
    if(this.frm.invalid) {
      this.markFormGroup(this.frm);
      return;
    }
    this.config.data.loading = true;
    this.service.createOrganization(this.frm.value).subscribe({
      next: (res) => {
        this.config.data.loading = false;
        this.messagingService.add({ severity: 'success', summary: 'organization_created', detail: 'you_have_now_access_to_dashboard' });
        this.ref.close();
      },
      error: (err) => {
        this.config.data.loading = false;
        this.highlightErrors(this.frm, err);
      }
    })
  }

}
