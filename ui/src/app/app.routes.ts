import { Routes } from '@angular/router';
import { ClientLayoutComponent } from './client/layout/client-layout.component';
import { LandingComponent } from './client/landing/landing.component';

export const routes: Routes = [
    { path: '', component: ClientLayoutComponent, children: [
        {path: '', component: LandingComponent}
    ] },
];
