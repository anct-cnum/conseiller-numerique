import { Component, OnInit } from '@angular/core';
import {ApiService} from 'app/core/services/api/api.service';
import {Observable} from 'rxjs';


@Component({
  selector: 'app-page-coach-confirm-email',
  templateUrl: './page-coach-confirm-email.component.html',
  styleUrls: ['./page-coach-confirm-email.component.scss']
})
export class PageCoachConfirmEmailComponent implements OnInit {

  constructor(
    private api: ApiService,
  ) { }

  ngOnInit(): void {
  }

  fnConfirm(key: string): Observable<any> {
    return this.api.confirmCoachEmail(key);
  }
}
