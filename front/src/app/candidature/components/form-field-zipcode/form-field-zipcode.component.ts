import {Component, Input, OnInit} from '@angular/core';
import {concat, Observable, of, Subject} from 'rxjs';
import {catchError, distinctUntilChanged, map, switchMap, tap} from 'rxjs/operators';
import {GeogouvService} from 'app/core/services/api/geogouv.service';
import {FormGroup} from '@angular/forms';
import {GeoCommune, ZipCodeWithCommune} from 'app/core/dao/geocommune';


export interface OptionCommune {
  label: string;
  commune: GeoCommune;
  zipCode: string;
}


@Component({
  selector: 'app-form-field-zipcode',
  templateUrl: './form-field-zipcode.component.html',
  styleUrls: ['./form-field-zipcode.component.scss']
})
export class FormFieldZipcodeComponent implements OnInit {
  @Input()
  form: FormGroup;

  @Input()
  key: string;

  @Input()
  label: string;

  @Input()
  required: boolean;

  @Input()
  helpText: string;

  zipCodes$: Observable<OptionCommune[]>;
  zipCodesLoading = false;
  zipCodesInput$ = new Subject<string>();

  constructor(
    private geoApi: GeogouvService,
  ) {}

  ngOnInit(): void {
    this.loadZipCodes();
  }

  private loadZipCodes(): void {
    this.zipCodes$ = concat(
      of([]), // default items
      this.zipCodesInput$.pipe(
        distinctUntilChanged(),
        tap(() => this.zipCodesLoading = true),
        switchMap(term => term?.length < 3 ? [] : this.geoApi.autocompleteCommunes(term).pipe(
          map(zipCodes => zipCodes.slice(0, 20).map((zipCodeWithCommune: ZipCodeWithCommune): OptionCommune => ({
              label: zipCodeWithCommune.zipCode + ' ' + zipCodeWithCommune.commune.name,
              zipCode: zipCodeWithCommune.zipCode,
              commune: zipCodeWithCommune.commune,
            })
          )),
          catchError((err) => {
            console.error(err);
            return of([]);
          }), // empty list on error
          tap(() => this.zipCodesLoading = false)
        ))
      )
    );
  }

}
