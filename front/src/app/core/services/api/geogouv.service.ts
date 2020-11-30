import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {ToastrService} from 'ngx-toastr';
import {DEFAULT_MESSAGE_CONFIG, MessageConfig} from './api.service';
import {forkJoin, Observable} from 'rxjs';
import {map, shareReplay, tap} from 'rxjs/operators';
import {GeoCommune, ZipCodeWithCommune} from 'app/core/dao/geocommune';
import {api2geoPoint} from './utils';

const API_FIELDS_QS = 'fields=nom,code,codesPostaux,centre,population,codeDepartement,codeRegion';

@Injectable({
  providedIn: 'root'
})
export class GeogouvService {

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

  searchCommunesByZipCode(zipCode: string,
                          messages: MessageConfig = DEFAULT_MESSAGE_CONFIG,
  ): Observable<GeoCommune[]> {
    return this.http.get(`https://geo.api.gouv.fr/communes?codePostal=${zipCode}&${API_FIELDS_QS}`)
      .pipe(
        tap({error: (error) => this.errorHandler(error, messages)}),
        map((jsonList: any) => jsonList.map(json => this.adapt2app_GeoCommune(json))),
        shareReplay(1),
      );
  }

  searchCommunesByName(name: string,
                       messages: MessageConfig = DEFAULT_MESSAGE_CONFIG,
  ): Observable<GeoCommune[]> {
    return this.http.get(`https://geo.api.gouv.fr/communes?nom=${name}&${API_FIELDS_QS}`)
      .pipe(
        tap({error: (error) => this.errorHandler(error, messages)}),
        map((jsonList: any) => jsonList.map(json => this.adapt2app_GeoCommune(json))),
        shareReplay(1),
      );
  }

  autocompleteCommunes(term: string,
                       messages: MessageConfig = DEFAULT_MESSAGE_CONFIG,
  ): Observable<ZipCodeWithCommune[]> {
    return forkJoin([
        this.searchCommunesByZipCode(term),
        this.searchCommunesByName(term),
      ]
    ).pipe(
      map(([res1, res2]) => this.flatCommunes([...res1, ...res2])),
    );
  }

  adapt2app_GeoCommune(json: any): GeoCommune {
    return {
      name: json.nom,
      code: json.code,
      zipCodes: json.codesPostaux,
      departementCode: json.codeDepartement,
      regionCode: json.codeRegion,
      center: api2geoPoint(json.centre),
    };
  }

  flatCommunes(communes: GeoCommune[]): ZipCodeWithCommune[] {
    const res = [];
    for (const commune of communes) {
      for (const zipCode of commune.zipCodes) {
        res.push({ zipCode, commune });
      }
    }
    console.log('zips', res);
    return res;
  }
}

