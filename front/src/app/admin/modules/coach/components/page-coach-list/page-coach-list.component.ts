import { Component, OnInit } from '@angular/core';
import {Observable} from 'rxjs';
import {CoachOutput} from 'app/core/dao/coach';
import {BoApiService} from "app/core/services/api/bo-api.service";


@Component({
  selector: 'app-page-coach-list',
  templateUrl: './page-coach-list.component.html',
  styleUrls: ['./page-coach-list.component.scss']
})
export class PageCoachListComponent implements OnInit {

  coaches$: Observable<CoachOutput[]>;

  constructor(
    private boApi: BoApiService,
  ) { }

  ngOnInit(): void {
    this.coaches$ = this.boApi.coachList();
  }

}
