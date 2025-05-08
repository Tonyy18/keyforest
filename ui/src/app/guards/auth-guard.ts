import { inject, Injectable } from "@angular/core";
import { ActivatedRouteSnapshot, CanActivate, CanActivateFn, GuardResult, MaybeAsync, Router, RouterStateSnapshot } from "@angular/router";
import { AuthService } from "../services/auth.service";
import { Observable } from "rxjs";

export const authGuard: CanActivateFn = (
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot,
  ) => {
    if(inject(AuthService).isTokenExpired() === false) {
        return true;
    }
    inject(Router).navigate(["/"])
    return false;
  };