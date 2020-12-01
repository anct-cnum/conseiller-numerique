import { Component, OnInit } from '@angular/core';
import {Observable} from 'rxjs';
import {ApiService} from 'app/core/services/api/api.service';

@Component({
  selector: 'app-page-host-confirm-email',
  templateUrl: './page-host-confirm-email.component.html',
  styleUrls: ['./page-host-confirm-email.component.scss']
})
export class PageHostConfirmEmailComponent implements OnInit {

  constructor(
    private api: ApiService,
  ) { }

  ngOnInit(): void {
  }

  fnConfirm(key: string): Observable<any> {
    return this.api.confirmHostEmail(key);
  }

}
