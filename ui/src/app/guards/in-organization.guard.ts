import { inject } from "@angular/core";
import { ActivatedRouteSnapshot, CanActivateFn, Router, RouterStateSnapshot } from "@angular/router";
import { AuthService } from "../services/auth.service";
import { hasConnectionGuard } from "./has-connection.guard";
import { DashboardService } from "../services/dashboard.service";
import { MessagingService } from "../services/messaging.service";

export const inOrganizationGuard: CanActivateFn = (
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot,
  ) => {
    const messaging = inject(MessagingService);
    if(hasConnectionGuard(route, state) === true) {
      const connections = inject(AuthService).user!.connections;
      const orgId = route.params?.["id"];
      const orgConnections = connections.filter(c => c.organization.id == orgId)
      if(orgConnections.length > 0) {
        inject(DashboardService).setActive(orgConnections[0].organization);
        inject(AuthService).user!.connections
        return true;
      } 
      /*else {
        messaging.add({
          severity: "error",
          summary: "access_denied",
          detail: "your_are_not_part_of_the_organization"
        });
      }*/
    }
    inject(Router).navigate(["/dashboard"]);
    return false;
};