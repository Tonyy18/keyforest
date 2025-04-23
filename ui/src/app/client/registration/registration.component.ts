import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { BaseComponent } from '../../shared/base.component';
import {MessagesModule} from 'primeng/messages';
import {MessageModule} from 'primeng/message';

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
      MessagesModule,
      MessageModule
    ],
    templateUrl: './registration.component.html',
    styleUrl: './registration.component.scss'
})
export class RegistrationComponent extends BaseComponent {

  protected frm: FormGroup;
  
  ngOnInit(): void {
    this.frm = this.fb.group({
      firstName: [undefined, [Validators.required, Validators.min(2), Validators.max(30)]],
      lastName: [undefined, [Validators.required, Validators.min(2), Validators.max(30)]],
      email: [undefined, [Validators.required, Validators.email]],
      password: [undefined, [Validators.required, Validators.min(6), Validators.max(30)]],
    })
  }

  protected save(): void {
    console.log("save");
    if(this.frm.invalid) {
      console.log("invalid");
      this.frm.markAllAsTouched();
      return;
    };
  }

}
