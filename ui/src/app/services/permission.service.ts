import { Injectable } from '@angular/core';
import { BaseService } from './base.service';
import { Observable, shareReplay } from 'rxjs';
import { Permission } from '../types/permission.type';

@Injectable({
  providedIn: 'root'
})
export class PermissionService extends BaseService {

  private permissions$: Observable<Permission[]>;
  
  getAll(): Observable<Permission[]> {
    if (!this.permissions$) {
      this.permissions$ = this.http.get<Permission[]>(this.apiUrl + "/permissions/")
        .pipe(shareReplay(1));
    }
    return this.permissions$;
  }

}