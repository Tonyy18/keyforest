import { Component, inject } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { ButtonModule } from 'primeng/button';
import { CheckboxModule } from 'primeng/checkbox';
import { InputTextModule } from 'primeng/inputtext';
import { AuthService } from '../../services/auth.service';
import { BaseComponent } from '../../shared/base.component';

@Component({
    selector: 'app-login',
    imports: [
      ButtonModule,
      TranslateModule,
      CheckboxModule,
      InputTextModule,
      RouterLink,
      FormsModule
    ],
    templateUrl: './login.component.html',
    styleUrl: './login.component.scss'
})
export class LoginComponent extends BaseComponent {
  protected email: string;
  protected password: string;
  protected loading: boolean = false;
  protected redirect: string;
  constructor(private route: ActivatedRoute, private authService: AuthService) {
    super();
    this.route.queryParams.subscribe(params => {
      this.email = params['email'];
      this.redirect = params['redirect'];
    });
  }

  login(): void {
    if(!this.email || !this.password) return;
    this.loading = true;
    this.authService.login({email: this.email, password: this.password}).subscribe({
      next: () => {
        this.loading = false;
        this.authService.getUser().subscribe({
          next: (user) => {
            if(user) {
              this.router.navigate([this.redirect ? this.redirect : "/"])
            }
          }
        });
      },
      error: () => {
        this.loading = false;
        this.messagingService.add({severity: "error", summary: "wrong_email_or_password", detail: "check_your_credentails"})
      }
    })
  }
}
