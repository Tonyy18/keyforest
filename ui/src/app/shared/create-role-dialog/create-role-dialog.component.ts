import { Component, inject } from '@angular/core';
import { FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { ButtonModule } from 'primeng/button';
import { DynamicDialogConfig, DynamicDialogRef } from 'primeng/dynamicdialog';
import { InputTextModule } from 'primeng/inputtext';
import { TextareaModule } from 'primeng/textarea';
import { BaseComponent } from '../base.component';
import { FormControlDirective } from '../../directives/form-control.directive';
import { PermissionService } from '../../services/permission.service';
import { Permission } from '../../types/permission.type';
import { MultiSelectModule } from 'primeng/multiselect';

@Component({
    selector: 'app-create-role-dialog',
    imports: [
      ButtonModule,
      TranslateModule,
      InputTextModule,
      TextareaModule,
      ReactiveFormsModule,
      FormControlDirective,
      MultiSelectModule
    ],
    templateUrl: './create-role-dialog.component.html',
    styleUrl: './create-role-dialog.component.scss'
})
export class CreateRoleDialogComponent extends BaseComponent {

  public config: DynamicDialogConfig = inject(DynamicDialogConfig);
  private ref: DynamicDialogRef = inject(DynamicDialogRef);
  permissionService: PermissionService = inject(PermissionService);
  permissions: Permission[] = [];
  
  frm: FormGroup = this.fb.group({
    name: [undefined, [Validators.required, Validators.minLength(3), Validators.maxLength(50)]],
    description: [undefined, Validators.maxLength(50)],
    permissions: [undefined, Validators.required],
  })

  ngOnInit(): void {
    this.permissionService.getAll().subscribe({
      next: (data: Permission[]) => {
        this.permissions = data;
      }
    })
    //For footer
    this.config.data ? this.config.data.save = () => {
      this.save();
    } : this.config.data = { save: () => { this.save(); } };
  }

  save(): void {
    this.config.data.loading = true;
    console.log(this.frm.value)
  }

}
