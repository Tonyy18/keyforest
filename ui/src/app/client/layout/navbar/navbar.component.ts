import { Component } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';
import { AvatarModule } from 'primeng/avatar';
import { ButtonModule } from 'primeng/button';
import { StyleClassModule } from 'primeng/styleclass';


@Component({
    selector: 'app-navbar',
    imports: [
        AvatarModule,
        StyleClassModule,
        ButtonModule,
        TranslateModule
    ],
    templateUrl: './navbar.component.html'
})
export class NavbarComponent {

}
