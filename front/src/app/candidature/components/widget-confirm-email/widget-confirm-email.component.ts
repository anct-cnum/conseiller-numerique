import {Component, Input, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Observable} from 'rxjs';

@Component({
  selector: 'app-widget-confirm-email',
  templateUrl: './widget-confirm-email.component.html',
  styleUrls: ['./widget-confirm-email.component.scss']
})
export class WidgetConfirmEmailComponent implements OnInit {

  @Input() fnConfirm: (key: string) => Observable<any>;

  key: string;
  ladda: boolean;
  isConfirmed: boolean;
  error: boolean;

  constructor(
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
    this.fnConfirm(this.key).subscribe(
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
