import { Component, OnInit } from '@angular/core';
import {ApiService} from 'app/core/services/api/api.service';
import {Observable} from 'rxjs';


@Component({
  selector: 'app-page-coach-confirm-email',
  templateUrl: './page-coach-confirm-email.component.html',
  styleUrls: ['./page-coach-confirm-email.component.scss']
})
export class PageCoachConfirmEmailComponent implements OnInit {

  isHost: boolean;

  constructor(
    private api: ApiService,
  ) { }

  ngOnInit(): void {
   this.isHost = false;
  }

  fnConfirm(key: string): Observable<any> {
    return this.api.confirmCoachEmail(key);
  }
}
