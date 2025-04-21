import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './navbar/navbar.component';

@Component({
    selector: 'app-client-layout',
    imports: [
      RouterOutlet,
      NavbarComponent
    ],
    templateUrl: './client-layout.component.html',
    styleUrl: './client-layout.component.scss'
})
export class ClientLayoutComponent {
  title = 'ui';
}
