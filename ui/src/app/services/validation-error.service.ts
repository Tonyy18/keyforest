import { Injectable } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
@Injectable({
  providedIn: 'root'
})
export class ValidationErrorService {
  
  constructor(private translate: TranslateService) {

  }

  getError(key: string, errors: any): string {
    let text = this.translate.instant("validation_errors." + key);
    if(typeof errors[key] === 'object') {
      text = text.replace("{requiredLength}", errors[key].requiredLength);
    }
    return text;
  }

}