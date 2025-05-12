import { Component, inject } from '@angular/core';
import { RouterLinkActive, RouterModule, RouterOutlet } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { IconFieldModule } from 'primeng/iconfield';
import { InputIconModule } from 'primeng/inputicon';
import { AvatarModule } from 'primeng/avatar';
import { AuthService } from '../../services/auth.service';
import { TranslateModule } from '@ngx-translate/core';
import { StyleClassModule } from 'primeng/styleclass';
import { DashboardService } from '../../services/dashboard.service';
import { CommonModule } from '@angular/common';

type DashboardLink = {
  routerLink: string,
  label: string,
  icon: string,
  secured?: boolean
}

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
      RouterLinkActive,
      CommonModule,
      RouterModule
    ],
    templateUrl: './dashboard-layout.component.html',
    styleUrl: './dashboard-layout.component.scss'
})
export class DashboardLayoutComponent {

  authService: AuthService = inject(AuthService);
  dashboardService: DashboardService = inject(DashboardService)

  links: DashboardLink[] = [
    {
      routerLink: "/dashboard",
      label: "organizations",
      icon: "pi-building",
    },
    {
      routerLink: "/roles",
      label: "roles",
      icon: "pi-building-columns",
      secured: true
    },
    {
      routerLink: "/applications",
      label: "applications",
      icon: "pi-desktop",
      secured: true
    }
  ]

  ngOnInit(): void {
    this.dashboardService.initActive();
  }

}
