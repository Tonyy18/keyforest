import { inject, Injectable } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { MessageService } from 'primeng/api';

@Injectable({
  providedIn: 'root'
})
export class MessagingService {
  
  private translate: TranslateService = inject(TranslateService);
  private messageService: MessageService = inject(MessageService);

  add(msg: {severity: string, summary?: string, detail?: string}): void {
    console.log("addmessage")
    this.messageService.add({
      severity: msg.severity,
      summary: msg.summary ? this.translate.instant(msg.summary) : null,
      detail: msg.detail ? this.translate.instant(msg.detail) : null
    })
  }

}