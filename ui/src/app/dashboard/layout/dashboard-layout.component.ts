import { Component, inject } from '@angular/core';
import { RouterLinkActive, RouterOutlet } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { IconFieldModule } from 'primeng/iconfield';
import { InputIconModule } from 'primeng/inputicon';
import { AvatarModule } from 'primeng/avatar';
import { AuthService } from '../../services/auth.service';
import { TranslateModule } from '@ngx-translate/core';
import { StyleClassModule } from 'primeng/styleclass';

@Component({
    selector: 'app-dashboard-layout',
    imports: [
      RouterOutlet,
      InputTextModule,
      IconFieldModule,
      InputIconModule,
      AvatarModule,
      TranslateModule,
      StyleClassModule,
      RouterLinkActive
    ],
    templateUrl: './dashboard-layout.component.html',
    styleUrl: './dashboard-layout.component.scss'
})
export class DashboardLayoutComponent {
  authService: AuthService = inject(AuthService);
}
