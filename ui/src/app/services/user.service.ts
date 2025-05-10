import { inject, Injectable } from '@angular/core';
import { BaseService } from './base.service';
import { Observable } from 'rxjs';
import { User } from '../types/user.type';
import { Organization } from '../types/organization.type';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class UserService extends BaseService{
  
  private authService = inject(AuthService);

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.apiUrl + "/users");
  }

  createUser(user: User): Observable<User> {
    return this.http.post<User>(this.apiUrl + "/users/", user);
  }

  addConnection(org: Organization) {
    this.authService.user?.connections.push(
      {
        id: 0,
        organization: org,
      }
    )
  }

}