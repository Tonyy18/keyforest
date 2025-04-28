import { Routes } from '@angular/router';
import { ClientLayoutComponent } from './client/layout/client-layout.component';
import { LandingComponent } from './client/landing/landing.component';
import { LoginComponent } from './client/login/login.component';
import { RegistrationComponent } from './client/registration/registration.component';
import { loggedOutGuard } from "./guards/logged-out.guard";
import { authGuard } from './guards/auth-guard';
import { StartOrganizationComponent } from './client/start-organization/start-organization.component';


export const routes: Routes = [
    { path: '', component: ClientLayoutComponent, children: [
        {path: '', component: LandingComponent},
        {path: 'login', component: LoginComponent, canActivate: [loggedOutGuard]},
        {path: 'register', component: RegistrationComponent, canActivate: [loggedOutGuard]},
        {path: 'start-organization', component: StartOrganizationComponent},
    ] },
];
