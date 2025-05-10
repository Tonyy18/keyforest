import { inject, Injectable } from '@angular/core';
import { UserConnection } from '../types/user-connection.type';
import { Organization } from '../types/organization.type';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  
  activeOrganization: Organization | undefined;
  userService: AuthService = inject(AuthService);
  
  setActive(org: Organization) {
    this.activeOrganization = org;
    localStorage.setItem("activeOrganization", org.id.toString());
  }

  initActive(): void {
    const storage = localStorage.getItem("activeOrganization");
    if(storage != undefined && storage != null) {
      try {
        const id = parseInt(storage);
        this.activeOrganization = this.userService.user?.connections.filter(c => c.organization.id == id)?.[0].organization;
      } catch(e) {
        console.error("Failed to set active organization from local storage")
      }
    }
  }

}