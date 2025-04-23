import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { BaseComponent } from '../../shared/base.component';
import { FormControlDirective } from '../../shared/form-control.directive';

@Component({
    selector: 'app-registration',
    imports: [
      ButtonModule,
      TranslateModule,
      InputTextModule,
      RouterLink,
      PasswordModule,
      FormsModule,
      ReactiveFormsModule,
      FormControlDirective
    ],
    templateUrl: './registration.component.html',
    styleUrl: './registration.component.scss'
})
export class RegistrationComponent extends BaseComponent {

  protected frm: FormGroup;
  
  ngOnInit(): void {
    this.frm = this.fb.group({
      firstName: [undefined, [Validators.required, Validators.minLength(2), Validators.maxLength(30)]],
      lastName: [undefined, [Validators.required, Validators.minLength(2), Validators.maxLength(30)]],
      email: [undefined, [Validators.required, Validators.email]],
      password: [undefined, [Validators.required, Validators.minLength(6), Validators.maxLength(30)]],
      password2: [undefined, [Validators.required, Validators.minLength(6), Validators.maxLength(30)]],
    })
  }

  protected save(): void {
    if(this.frm.invalid) {
      this.markFormGroup(this.frm);
      return;
    };
  }

}
