import { inject, Injectable } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { MessageService } from 'primeng/api';

@Injectable({
  providedIn: 'root'
})
export class MessagingService {
  
  private translate: TranslateService = inject(TranslateService);
  private messageService: MessageService = inject(MessageService);

  add(msg: {severity: string, summary?: string, detail?: string, summaryMapping?: Record<string, string>, detailMapping?: Record<string, string>}): void {

    let summary = msg.summary ? this.translate.instant(msg.summary) : null;
    let detail = msg.detail ? this.translate.instant(msg.detail) : null;
    if(summary && msg.summaryMapping) {
      for (const [key, value] of Object.entries(msg.summaryMapping)) {
        summary = summary.replace("{" + key + "}", value);
      }
    }

    if(detail && msg.detailMapping) {
      for (const [key, value] of Object.entries(msg.detailMapping)) {
        detail = detail.replace("{" + key + "}", value);
      }
    }

    this.messageService.add({
      severity: msg.severity,
      summary: summary,
      detail: detail
    })
  }

}