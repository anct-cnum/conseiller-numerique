import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

import {map, shareReplay, tap} from 'rxjs/operators';
import { ToastrService } from 'ngx-toastr';

import { environment } from '@env';
import {Observable} from 'rxjs';
import {CoachInput, CoachOutput} from 'app/core/dao/coach';
import {ApiAdapter} from './adapter';
import {
  HostOrganizationInput,
  HostOrganizationOutput
} from 'app/core/dao/hostorganization';
import {MatchingOutput} from 'app/core/dao/matching';


export interface MessageConfig {
  onBadInput?: (error) => string;
  onUnauthorized?: (error) => string;
  onServerError?: (error) => string;
  onUnexpectedError?: (error) => string;
}


export const DEFAULT_MESSAGE_CONFIG: MessageConfig = {
  // 400
  onBadInput: (error) => {
    if (error.error.non_field_errors && error.error.non_field_errors.length > 0) {
      const msg = error.error.non_field_errors[0];
      return msg.slice(0, 150);
    }
    return 'Entrée invalide';
  },
  // 403
  onUnauthorized: (error) => 'Droits insuffisant pour effectuer cette action',
  // 500
  onServerError: (error) => `Une erreur est survenue : ${error.message}`,
  // default
  onUnexpectedError: (error) => `Une erreur est survenue : ${error.message}`,
};


@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(
    protected http: HttpClient,
    protected toastrService: ToastrService,
  ) {}

  protected errorHandler(error, messages: MessageConfig): void {
    if (error.status === 400 && messages.onBadInput) {
      this.toastrService.error(messages.onBadInput(error));
    }
    else if (error.status === 403 && messages.onUnauthorized) {
      this.toastrService.error(messages.onUnauthorized(error));
    }
    else if (error.status === 500 && messages.onServerError) {
      this.toastrService.error(messages.onServerError(error));
    }
    else if (messages.onUnexpectedError) {
      this.toastrService.error(messages.onUnexpectedError(error));
    }
  }

  postCoachApplication(resource: CoachInput,
                       messages: MessageConfig = DEFAULT_MESSAGE_CONFIG,
  ): Observable<CoachOutput> {
    const data = ApiAdapter.app2api(resource);
    return this.http.post(`${environment.apiUrl}/api/coaches.add`, data)
      .pipe(
        tap({error: (error) => this.errorHandler(error, messages)}),
        map((json: any) => ApiAdapter.api2app(json)),
        shareReplay(1),
      );
  }

  postHostingOrganizationApplication(resource: HostOrganizationInput,
                                     messages: MessageConfig = DEFAULT_MESSAGE_CONFIG,
  ): Observable<HostOrganizationOutput> {
    const data = ApiAdapter.app2api(resource);
    return this.http.post(`${environment.apiUrl}/api/hostorganizations.add`, data)
      .pipe(
        tap({error: (error) => this.errorHandler(error, messages)}),
        map((json: any) => ApiAdapter.api2app(json)),
        shareReplay(1),
      );
  }

  getMatchingByKey(key: string,
                   messages: MessageConfig = DEFAULT_MESSAGE_CONFIG,
  ): Observable<MatchingOutput> {
    return this.http.get(`${environment.apiUrl}/api/matchings.get_by_key/${key}`)
      .pipe(
        tap({error: (error) => this.errorHandler(error, messages)}),
        map((json: any) => ApiAdapter.api2app(json)),
        shareReplay(1),
      );
  }

  confirmCoachEmail(key: string,
                    messages: MessageConfig = DEFAULT_MESSAGE_CONFIG,
  ): Observable<any> {
    return this.http.post(`${environment.apiUrl}/api/coach.confirm_email`, {key})
      .pipe(
        tap({error: (error) => this.errorHandler(error, messages)}),
        map((json: any) => ApiAdapter.api2app(json)),
        shareReplay(1),
      );
  }

  confirmHostEmail(key: string,
                   messages: MessageConfig = DEFAULT_MESSAGE_CONFIG,
  ): Observable<any> {
    return this.http.post(`${environment.apiUrl}/api/hostorganization.confirm_email`, {key})
      .pipe(
        tap({error: (error) => this.errorHandler(error, messages)}),
        map((json: any) => ApiAdapter.api2app(json)),
        shareReplay(1),
      );
  }
}
