import { Component, OnInit } from '@angular/core';
import {ApiService} from 'app/core/services/api/api.service';
import {MatchingOutput} from 'app/core/dao/matching';
import {ActivatedRoute} from '@angular/router';
import {environment} from '@env';
import {HttpErrorResponse} from '@angular/common/http';


@Component({
  selector: 'app-matching',
  templateUrl: './page-matching.component.html',
  styleUrls: ['./page-matching.component.scss']
})
export class PageMatchingComponent implements OnInit {
  isLoading: boolean;
  matching: MatchingOutput;
  mode: string;
  errorNotFound: boolean;
  setMeetingDone: boolean;

  constructor(
    private route: ActivatedRoute,
    private api: ApiService,
  ) { }

  ngOnInit(): void {
    this.isLoading = true;
    this.errorNotFound = false;
    this.route.params.subscribe(
      params => {
        this.mode = params.mode;
        if (params.key) {
          this.api.getMatchingByKey(params.key).subscribe(
            matching => {
              if (this.mode === 'coach' && !matching.hostMeetingOk) {
                this.errorNotFound = true;
                this.matching = null;
              }
              else {
                this.matching = matching;
              }
              this.isLoading = false;
            },
            (error: HttpErrorResponse) => {
              console.error('Error getting page-matching', error);
              if (error.status === 404) {
                this.errorNotFound = true;
              }
              this.isLoading = false;
            }
          );
        }
      }
    );
  }

  isModeHost(): boolean {
    return this.mode !== 'coach';
  }

  isModeCoach(): boolean {
    return this.mode === 'coach';
  }

  getBooleanText(b: boolean): string {
    return b ? 'Oui' : 'Non';
  }

  get debug(): boolean {
    return !environment.production || this.route.snapshot.queryParams.debug === '1';
  }

  setMeeting(value: boolean): void {
    this.isLoading = true;
    this.setMeetingDone = false;
    this.api.setMeeting({key: this.matching.key, value}).subscribe(
      _ => {
        this.isLoading = false;
        this.setMeetingDone = true;
        this.matching.hostMeetingOk = value;
      },
      err => {
        this.isLoading = false;
      }
    );
  }
}
