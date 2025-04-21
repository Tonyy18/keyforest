import { Routes } from '@angular/router';
import { ClientLayoutComponent } from './client/layout/client-layout.component';
import { LandingComponent } from './client/landing/landing.component';
import { LoginComponent } from './client/login/login.component';

export const routes: Routes = [
    { path: '', component: ClientLayoutComponent, children: [
        {path: '', component: LandingComponent},
        {path: 'login', component: LoginComponent}
    ] },
];
