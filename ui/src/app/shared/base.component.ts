import { inject } from "@angular/core";
import { FormBuilder } from "@angular/forms";
import { TranslateService } from "@ngx-translate/core";

export abstract class BaseComponent {
  protected translateService: TranslateService = inject(TranslateService);
  protected fb: FormBuilder = inject(FormBuilder);
}