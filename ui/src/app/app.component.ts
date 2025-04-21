import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {TranslateService} from "@ngx-translate/core";
import { TranslateModule } from '@ngx-translate/core';
import { ButtonModule } from 'primeng/button';

@Component({
    selector: 'app-root',
    imports: [
      RouterOutlet,
      TranslateModule
    ],
    templateUrl: './app.component.html',
    styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'ui';
  constructor(private translate: TranslateService) {
    this.translate.addLangs(['fi', 'en']);
    this.translate.setDefaultLang('en');
  }
}
