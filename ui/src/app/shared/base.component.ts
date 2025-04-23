import { inject } from "@angular/core";
import { FormBuilder, FormGroup } from "@angular/forms";
import { TranslateService } from "@ngx-translate/core";

export abstract class BaseComponent {
  protected translateService: TranslateService = inject(TranslateService);
  protected fb: FormBuilder = inject(FormBuilder);

  markFormGroup(frm: FormGroup): void {
    for(let key in frm.controls) {
      const control = frm.controls[key];
      if(control.invalid) {
        control.markAsDirty();
      }
    }
  }
}