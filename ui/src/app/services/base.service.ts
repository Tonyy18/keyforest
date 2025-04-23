import { inject } from '@angular/core';
import { environment } from '../../environments/environment.prod';
import { HttpClient } from '@angular/common/http';

export abstract class BaseService {
  protected apiUrl = environment.apiUrl
  protected http: HttpClient = inject(HttpClient);
}