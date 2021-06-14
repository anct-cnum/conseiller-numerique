import { Injectable } from '@angular/core';
import { HttpErrorResponse, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import {ApiAdapter} from "app/core/services/api/adapter";


@Injectable()
export class ErrorInterceptor implements HttpInterceptor {

  constructor(
    private router: Router,
    private toastr: ToastrService,
  ) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(catchError((err: HttpErrorResponse) => {
      this.handleErrorResponse(err);
      return throwError(err);
    }));
  }

  private handleErrorResponse(err: HttpErrorResponse): void {
    this._showBackendMessage(err);
    if (err.status === 401) {
      // Clear session information as they are outdated
      sessionStorage.clear();
      this.router.navigate(['/auth/login']);
    }
  }

  private _showBackendMessage(err: HttpErrorResponse): void {
    const messageToShow = this._generateErrorMessage(err);
    this.toastr.error(messageToShow);
  }

  private _generateErrorMessage(err: HttpErrorResponse): string {
    if (!err) {
      return 'Une erreur est survenue';
    }
    if (err.status === 400) {
      return 'Entrée invalide';
    }
    else if (err.status === 403) {
      return 'Droits insuffisant pour effectuer cette action';
    }
    else if (err.status === 404) {
      return 'Non trouvé';
    }
    else if (err.status === 409) {
      return `Votre inscription a déjà été enregistrée`;
    }
    else if (err.status === 500) {
      return `Une erreur est survenue : ${err.message}`;
    }
    else {
      return `Une erreur est survenue : ${err.message}`;
    }
  }
}
