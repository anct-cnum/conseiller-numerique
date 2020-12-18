import {Component, OnInit, ViewChild} from '@angular/core';
import {Observable, ReplaySubject, Subject} from 'rxjs';
import {CoachOutput} from 'app/core/dao/coach';
import {BoApiService} from 'app/core/services/api/bo-api.service';
import {FormControl} from '@angular/forms';
import {MatSelect} from "@angular/material/select";
import {takeUntil} from "rxjs/operators";


interface Zone {
  name: string;
}


@Component({
  selector: 'app-page-coach-list',
  templateUrl: './page-coach-list.component.html',
  styleUrls: ['./page-coach-list.component.scss']
})
export class PageCoachListComponent implements OnInit {

  displayedColumns = ['id', 'name', 'email', 'zipCode', 'emailVerified', 'isActive', 'actions'];
  coaches$: Observable<CoachOutput[]>;

  protected zones: Zone[] = [
    {name: 'Paris'},
    {name: 'Lyon'},
    {name: 'Bordeaux'},
  ];
  public zoneCtrl: FormControl = new FormControl();
  public zoneFilterCtrl: FormControl = new FormControl();
  public filteredZones$: ReplaySubject<Zone[]> = new ReplaySubject<Zone[]>(1);
  @ViewChild('zoneSelect', { static: true }) multiSelect: MatSelect;
  protected _onDestroy$ = new Subject<void>();


  constructor(
    private boApi: BoApiService,
  ) { }

  ngOnInit(): void {
    this.coaches$ = this.boApi.coachList();
    this.filteredZones$.next(this.zones.slice());

    // listen for search field value changes
    this.zoneFilterCtrl.valueChanges
      .pipe(takeUntil(this._onDestroy$))
      .subscribe(() => {
        this.filterZones();
      });
  }

  protected filterZones(): void {
    if (!this.zones) {
      return;
    }
    // get the search keyword
    let search = this.zoneFilterCtrl.value;
    if (!search) {
      this.filteredZones$.next(this.zones.slice());
      return;
    } else {
      search = search.toLowerCase();
    }
    // filter the banks
    this.filteredZones$.next(
      this.zones.filter(zone => zone.name.toLowerCase().indexOf(search) > -1)
    );
  }

  edit(row: CoachOutput): void {
    // TODO
  }
}
