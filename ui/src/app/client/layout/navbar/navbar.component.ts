import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { AvatarModule } from 'primeng/avatar';
import { ButtonModule } from 'primeng/button';
import { StyleClassModule } from 'primeng/styleclass';
import { AuthService } from '../../../services/auth.service';
import { CommonModule } from '@angular/common'; 

@Component({
    selector: 'app-navbar',
    imports: [
        AvatarModule,
        StyleClassModule,
        ButtonModule,
        TranslateModule,
        RouterLink,
        CommonModule
    ],
    templateUrl: './navbar.component.html'
})
export class NavbarComponent {
    protected authService: AuthService = inject(AuthService);
}
