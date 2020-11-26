import { Component, OnInit } from '@angular/core';
import {ApiService} from 'app/core/services/api/api.service';
import {ActivatedRoute} from '@angular/router';


@Component({
  selector: 'app-page-coach-confirm-email',
  templateUrl: './page-coach-confirm-email.component.html',
  styleUrls: ['./page-coach-confirm-email.component.scss']
})
export class PageCoachConfirmEmailComponent implements OnInit {

  key: string;
  ladda: boolean;
  isConfirmed: boolean;
  error: boolean;

  constructor(
    private api: ApiService,
    private route: ActivatedRoute,
  ) { }

  ngOnInit(): void {
    this.ladda = false;
    this.isConfirmed = false;
    this.error = false;
    this.route.params.subscribe(
      params => {
        this.key = params.key;
      }
    );
  }

  clickConfirm(): void {
    this.ladda = true;
    this.isConfirmed = false;
    this.error = false;
    this.api.confirmCoachEmail(this.key).subscribe(
      _ => {
        this.ladda = false;
        this.isConfirmed = true;
      },
      err => {
        this.ladda = false;
        this.error = true;
      }
    );
  }
}
