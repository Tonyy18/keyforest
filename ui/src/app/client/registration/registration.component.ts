import { Component, inject } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { BaseComponent } from '../../shared/base.component';
import { FormControlDirective } from '../../directives/form-control.directive';
import { UserService } from '../../services/user.service';
import { MessageService } from 'primeng/api';

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
      FormControlDirective,
    ],
    templateUrl: './registration.component.html',
    styleUrl: './registration.component.scss'
})
export class RegistrationComponent extends BaseComponent {

  protected frm: FormGroup;
  protected userService: UserService = inject(UserService);
  protected loading: boolean = false;
  
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
    if(this.frm.get("password")!.value != this.frm.get("password2")!.value) {
      this.frm.get("password2")?.setErrors({passwordMatches: true});
      this.frm.get("password2")?.markAsDirty();
      return
    }
    this.loading = true;
    this.userService.createUser(this.frm.value).subscribe({
      next: () => {
        this.messagingService.add({ severity: 'success', summary: 'account_created', detail: 'you_can_now_login' });
        this.loading = false;
        this.router.navigate(["/login"], {queryParams: {email: this.frm.get("email")!.value}})
      },
      error: (errors) => {
        this.loading = false;
        this.highlightErrors(this.frm, errors);
      }
    })
  }
}
