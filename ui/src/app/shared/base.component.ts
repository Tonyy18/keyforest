import { inject } from "@angular/core";
import { FormBuilder, FormGroup } from "@angular/forms";
import { TranslateService } from "@ngx-translate/core";
import { Router } from "@angular/router";
import { MessagingService } from "../services/messaging.service";

export abstract class BaseComponent {
  protected translateService: TranslateService = inject(TranslateService);
  protected messagingService: MessagingService = inject(MessagingService);
  protected router: Router = inject(Router);
  protected fb: FormBuilder = inject(FormBuilder);

  markFormGroup(frm: FormGroup): void {
    for(let key in frm.controls) {
      const control = frm.controls[key];
      if(control.invalid) {
        control.markAsDirty();
      }
    }
  }
  
  highlightErrors(frm: FormGroup, httpRes: any): void {
    if("error" in httpRes && typeof httpRes.error == "object") {
      const httpErrors: {[field: string] : string[] | string} = httpRes.error;
      for(let field in httpErrors) {
        if(Array.isArray(httpErrors[field])) {
          const errors: string[] = httpErrors[field];
          if(field in frm.controls && errors?.length > 0) {
            const setErrors: {[error: string] : boolean} = {}
            setErrors[errors[0]] = true;
            frm.controls[field].setErrors(setErrors)
            frm.controls[field].markAsDirty();
          }
        }
      }
    }
  }
}