import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { AvatarModule } from 'primeng/avatar';
import { ButtonModule } from 'primeng/button';
import { StyleClassModule } from 'primeng/styleclass';
import { AuthService } from '../../../services/auth.service';
import { CommonModule } from '@angular/common'; 
import { MessagingService } from '../../../services/messaging.service';

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
    protected messagingService: MessagingService = inject(MessagingService);
    protected logout(): void {
        this.authService.logout();
        this.messagingService.add({severity: "success", summary: "you_have_been_logged_out"})
    }
}
