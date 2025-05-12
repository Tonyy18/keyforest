import { inject, Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpErrorResponse } from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { MessagingService } from '../services/messaging.service';

@Injectable()
export class HttpErrorInterceptor implements HttpInterceptor {
  
  authService: AuthService = inject(AuthService);
  messaging: MessagingService = inject(MessagingService);

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(req).pipe(
      catchError((error: HttpErrorResponse) => {
        // 🔍 Inspect error
        if(error.error?.code == "token_not_valid") {
          this.authService.logout();
          this.messaging.add({
            severity: "error",
            summary: "login_session_expired",
            detail: "please_login_again"
          })
        }

        return throwError(() => error);
      })
    );
  }
}