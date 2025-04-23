import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { BaseComponent } from '../../shared/base.component';
import { FormControlDirective } from '../../directives/form-control.directive';
import { UserService } from '../../services/user.service';

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
      first_name: [undefined, [Validators.required, Validators.minLength(2), Validators.maxLength(30)]],
      last_name: [undefined, [Validators.required, Validators.minLength(2), Validators.maxLength(30)]],
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
        this.messageService.add({ severity: 'success', summary: 'Käyttäjä luotu', detail: 'Message Content' });
        this.loading = false;
      },
      error: (errors) => {
        this.loading = false;
        this.highlightErrors(this.frm, errors);
      }
    })
  }
}
