import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {ToastrService} from 'ngx-toastr';
import { environment } from '@env';
import {forkJoin, Observable} from 'rxjs';
import {map, shareReplay, tap} from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})

export class ApiEntreprise {

  constructor(
    protected http: HttpClient,
    protected toastrService: ToastrService,
  ) {}

  checkSiret(siret: string): Observable<any> {
    return this.http.get(`${environment.apiSiretUrl}/siret/${siret}`);
  }
}

