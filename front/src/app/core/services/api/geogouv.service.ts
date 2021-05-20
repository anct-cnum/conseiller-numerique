import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {ToastrService} from 'ngx-toastr';
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

  searchCommunesByZipCode(zipCode: string): Observable<GeoCommune[]> {
    let url = `https://geo.api.gouv.fr/communes?codePostal=${zipCode}&${API_FIELDS_QS}`;
    if (zipCode === '97150') {
      url = 'https://conseiller-numerique.cellar-c2.services.clever-cloud.com/geo/saint-martin.json';
    }
    return this.http.get(url)
      .pipe(
        map((jsonList: any) => jsonList.map(json => this.adapt2app_GeoCommune(json))),
        shareReplay(1),
      );
  }

  searchCommunesByName(name: string): Observable<GeoCommune[]> {
    let url = `https://geo.api.gouv.fr/communes?nom=${name}&${API_FIELDS_QS}`;
    if (name !== null && name.toLowerCase() === 'saint-martin') {
      url = 'https://conseiller-numerique.cellar-c2.services.clever-cloud.com/geo/saint-martin.json';
    }
    return this.http.get(url)
      .pipe(
        map((jsonList: any) => jsonList.map(json => this.adapt2app_GeoCommune(json))),
        shareReplay(1),
      );
  }

  autocompleteCommunes(term: string): Observable<ZipCodeWithCommune[]> {
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

