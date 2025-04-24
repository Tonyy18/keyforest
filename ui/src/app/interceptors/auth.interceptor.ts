import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Get the JWT token from localStorage (or wherever you store it)
    const token = localStorage.getItem('token');
    
    // If token exists, clone the request and add the Authorization header
    if (token) {
      const cloned = req.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });

      // Pass the cloned request with the Authorization header
      return next.handle(cloned);
    }

    // If no token exists, just pass the original request
    return next.handle(req);
  }
}