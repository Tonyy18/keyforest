import { inject, Injectable } from '@angular/core';
import { BaseService } from './base.service';
import { catchError, Observable, of, tap, throwError } from 'rxjs';
import { User } from '../types/user.type';
import {jwtDecode} from 'jwt-decode';
import { MessagingService } from './messaging.service';
import { Router } from '@angular/router';

export type Credentials = {
  email: string,
  password: string
}

export type JwtResponse = {
  refresh: string,
  access: string,
  user: User
}

@Injectable({
  providedIn: 'root'
})
export class AuthService extends BaseService{
  
  user?: User; //logged in user data
  messagingService: MessagingService = inject(MessagingService);
  router: Router = inject(Router);

  login(credentials: Credentials): Observable<any> {
    return this.http.post<JwtResponse>(this.apiUrl + "/auth/login/", credentials).pipe(
      tap(response => {
        localStorage.setItem("token", response.access);
        this.user = response.user;
      }),
      catchError(error => {
        return throwError(() => error);
      })
    );
  }

  logout(): void {
    localStorage.removeItem("token");
    this.user = undefined;
    this.router.navigate(["/login"]);
  }

  getUser(): Observable<User | null> {
    return this.http.get<User>(this.apiUrl + "/auth/me/").pipe(
      tap(response => {
        this.user = response;
      }),
      catchError(error => {
        return of(null)
      })
    );
  }
  
  isTokenExpired(): boolean | null {
    const token: string | null = localStorage.getItem("token");
    if(!token) {
      return null;
    }
    try {
      const decoded: any = jwtDecode(token);
      const exp = decoded.exp;
      const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds
  
      return exp < currentTime; // True if expired, false if valid
    } catch (error) {
      console.error('Error decoding token', error);
      return true; // Assume the token is expired if decoding fails
    }
  }

  isLoggedIn(): boolean {
    return this.isTokenExpired() !== true && this.user != null;
  }

}