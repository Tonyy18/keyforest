import { inject } from "@angular/core";
import { ActivatedRouteSnapshot, CanActivateFn, Router, RouterStateSnapshot } from "@angular/router";
import { AuthService } from "../services/auth.service";
import { authGuard } from "./auth-guard";

export const hasConnectionGuard: CanActivateFn = (
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot,
  ) => {
    if(authGuard(route, state) === true) {
      const connections = inject(AuthService).user!.connections;
      if(connections.length > 0) {
        return true;
      }
    }
    inject(Router).navigate(["/"]);
    return false;
};