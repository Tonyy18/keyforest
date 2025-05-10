import { APP_INITIALIZER, ApplicationConfig, importProvidersFrom, inject, provideAppInitializer, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import {HTTP_INTERCEPTORS, HttpClient, provideHttpClient, withInterceptorsFromDi} from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

import {TranslateModule, TranslateLoader} from "@ngx-translate/core";
import {TranslateHttpLoader} from '@ngx-translate/http-loader';

import { providePrimeNG } from 'primeng/config';
import Nora from '@primeng/themes/material';
import { routes } from './app.routes';
import { AuthInterceptor } from './interceptors/auth.interceptor';
import { HttpErrorInterceptor } from './interceptors/http-error.interceptor';
import { MessageService } from 'primeng/api';
import { DialogService } from 'primeng/dynamicdialog';
import { AuthService } from './services/auth.service';
import { catchError, Observable } from 'rxjs';

const httpLoaderFactory: (http: HttpClient) => TranslateHttpLoader = (http: HttpClient) =>
  new TranslateHttpLoader(http, './assets/lang/', '.json');

export function StartupServiceFactory(): void | Observable<unknown> | Promise<unknown> {
  const authService = inject(AuthService);
  return authService.getUser();
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideHttpClient(
      withInterceptorsFromDi()
    ),
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true,
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: HttpErrorInterceptor,
      multi: true,
    },
    provideRouter(routes),
    providePrimeNG({
      ripple: true,
      theme: {
        preset: Nora,
        options: {
          darkModeSelector: '.my-app-dark'
        }
      }
    }),
    provideAnimationsAsync(),
    importProvidersFrom([TranslateModule.forRoot({
      loader: {
        provide: TranslateLoader,
        useFactory: httpLoaderFactory,
        deps: [HttpClient],
      },
    })]),
    MessageService,
    DialogService,
    provideAppInitializer(StartupServiceFactory)
  ]
};
