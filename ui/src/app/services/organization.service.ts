import { Injectable } from '@angular/core';
import { BaseService } from './base.service';
import { Observable } from 'rxjs';
import { Organization } from '../types/organization.type';

@Injectable({
  providedIn: 'root'
})
export class OrganizationService extends BaseService {
  
  createOrganization(user: Organization): Observable<Organization> {
    return this.http.post<Organization>(this.apiUrl + "/organizations/", user);
  }

}