import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { ToastrService } from 'ngx-toastr';

import { environment } from '@env';
import {CoachInput, CoachOutput} from 'app/core/dao/coach';
import {
  HostOrganizationInput,
  HostOrganizationOutput
} from 'app/core/dao/hostorganization';
import {MatchingOutput} from 'app/core/dao/matching';
import {Unsubscribepayload} from 'app/core/dao/unsubscribepayload';
import {isArray} from 'app/utils/utils';
import {Observable} from 'rxjs';
import {SetInterviewResultPayload} from 'app/core/dao/setinterviewresultpayload';


@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(
    protected http: HttpClient,
    protected toastrService: ToastrService,
  ) {}

  postCoachApplication(resource: CoachInput): Observable<CoachOutput> {
    return this.http.post<CoachOutput>(`${environment.apiUrl}/api/coaches.add`, resource);
  }

  postHostingOrganizationApplication(resource: HostOrganizationInput): Observable<HostOrganizationOutput> {
    return this.http.post<HostOrganizationOutput>(`${environment.apiUrl}/api/hostorganizations.add`, resource);
  }

  getMatchingByKey(key: string): Observable<MatchingOutput> {
    return this.http.get<MatchingOutput>(`${environment.apiUrl}/api/matchings.get_by_key/${key}`);
  }

  confirmCoachEmail(key: string): Observable<any> {
    return this.http.post(`${environment.apiUrl}/api/coach.confirm_email`, {key});
  }

  confirmHostEmail(key: string): Observable<any> {
    return this.http.post(`${environment.apiUrl}/api/hostorganization.confirm_email`, {key});
  }

  unsubscribeCoach(payload: Unsubscribepayload): Observable<any> {
    return this.http.post(`${environment.apiUrl}/api/coach.unsubscribe`, payload);
  }

  unsubscribeHostOrganization(payload: Unsubscribepayload): Observable<any> {
    return this.http.post(`${environment.apiUrl}/api/hostorganization.unsubscribe`, payload);
  }

  setInterviewResult(payload: SetInterviewResultPayload): Observable<any> {
    return this.http.post(`${environment.apiUrl}/api/matching.set_interview_result`, payload);
  }

  flattenErrors(err: HttpErrorResponse): string[] {
    const errorMessages = [];
    if (err.status === 400) {
      console.log('error to flatten:', err.error);
      for (const [key, value] of Object.entries(err.error)) {
        let prefix = key + ' : ';
        if (key === 'non_field_errors') {
          prefix = '';
        }
        if (isArray(value)) {
          for (const msg of (value as any[])) {
            errorMessages.push(prefix + msg);
          }
        } else {
          errorMessages.push(prefix + value);
        }
      }
    }
    else {
      errorMessages.push('Erreur');
    }
    return errorMessages;
  }
}
