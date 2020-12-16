import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {ToastrService} from 'ngx-toastr';
import {CoachOutput} from 'app/core/dao/coach';
import {Observable} from 'rxjs';
import {environment} from '@env';


@Injectable({
  providedIn: 'root'
})
export class BoApiService {

  constructor(
    protected http: HttpClient,
    protected toastrService: ToastrService,
  ) {}

  coachList(): Observable<CoachOutput[]> {
    return this.http.get<CoachOutput[]>(`${environment.apiUrl}/bo/api/coaches/`);
  }
}
