import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { BaseComponent } from '../../shared/base.component';

@Component({
  selector: 'app-roles',
  imports: [
    CommonModule,
    ButtonModule,
    TranslateModule
  ],
  templateUrl: './roles.component.html',
  styleUrl: './roles.component.scss'
})
export class RolesComponent extends BaseComponent {


}
