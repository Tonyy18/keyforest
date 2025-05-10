import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {TranslateService} from "@ngx-translate/core";
import { TranslateModule } from '@ngx-translate/core';
import { ToastModule } from 'primeng/toast';
import { AuthService } from './services/auth.service';

@Component({
    selector: 'app-root',
    imports: [
      RouterOutlet,
      TranslateModule,
      ToastModule
    ],
    templateUrl: './app.component.html',
    styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'ui';
  constructor(private translate: TranslateService, private authService: AuthService) {
    this.translate.addLangs(['fi', 'en']);
    this.translate.setDefaultLang('en');
  }
}
