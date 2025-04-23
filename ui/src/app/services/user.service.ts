import { Injectable } from '@angular/core';
import { BaseService } from './base.service';
import { Observable } from 'rxjs';
import { User } from '../types/user.type';

@Injectable({
  providedIn: 'root'
})
export class UserService extends BaseService{
  
  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.apiUrl + "/users");
  }

  createUser(user: User): Observable<User> {
    return this.http.post<User>(this.apiUrl + "/users/", user);
  }

}