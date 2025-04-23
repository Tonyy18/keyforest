import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {TranslateService} from "@ngx-translate/core";
import { TranslateModule } from '@ngx-translate/core';
import { MessageService } from 'primeng/api';
import { ToastModule } from 'primeng/toast';

@Component({
    selector: 'app-root',
    imports: [
      RouterOutlet,
      TranslateModule,
      ToastModule
    ],
    templateUrl: './app.component.html',
    styleUrl: './app.component.scss',
    providers: [MessageService]
})
export class AppComponent {
  title = 'ui';
  constructor(private translate: TranslateService) {
    this.translate.addLangs(['fi', 'en']);
    this.translate.setDefaultLang('fi');
  }
}
