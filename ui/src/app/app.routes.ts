import { Routes } from '@angular/router';
import { ClientLayoutComponent } from './client/layout/client-layout.component';
import { LandingComponent } from './client/landing/landing.component';
import { LoginComponent } from './client/login/login.component';
import { RegistrationComponent } from './client/registration/registration.component';
import { loggedOutGuard } from "./guards/logged-out.guard";
import { authGuard } from './guards/auth-guard';
import { StartOrganizationComponent } from './client/start-organization/start-organization.component';
import { DashboardLayoutComponent } from './dashboard/layout/dashboard-layout.component';
import { OrganizationsComponent } from './dashboard/organizations/organizations.component';
import { hasConnectionGuard } from './guards/dashboard.guard';


export const routes: Routes = [
    { path: '', component: ClientLayoutComponent, children: [
        {path: '', component: LandingComponent},
        {path: 'login', component: LoginComponent, canActivate: [loggedOutGuard]},
        {path: 'register', component: RegistrationComponent, canActivate: [loggedOutGuard]},
        {path: 'start-organization', component: StartOrganizationComponent, canActivate: [authGuard]},
    ] },
    { path: 'dashboard', component: DashboardLayoutComponent, children: [
        {path: '', component: OrganizationsComponent, canActivate: [hasConnectionGuard]}
    ] },
];
