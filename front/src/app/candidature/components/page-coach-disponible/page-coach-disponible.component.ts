import { Component, OnInit } from '@angular/core';
import {ApiService} from 'app/core/services/api/api.service';
import {environment} from '@env';
import {ActivatedRoute} from '@angular/router';
import {ToastrService} from 'ngx-toastr';
import {Disponiblepayload} from 'app/core/dao/disponiblepayload';


@Component({
  selector: 'app-page-coach-disponible',
  templateUrl: './page-coach-disponible.component.html',
  styleUrls: ['./page-coach-disponible.component.scss']
})
export class PageCoachDisponibleComponent implements OnInit {

  errorMessages: string[];
  ladda: boolean;
  key: string;
  disponible: string;

  constructor(
    private api: ApiService,
    private route: ActivatedRoute,
    private toast: ToastrService,
  ) { }

  ngOnInit(): void {
    this.errorMessages = [];
    this.ladda = false;
    this.route.params.subscribe(
      params => {
        this.key = params.key || null;
        this.disponible = params.disponible || null;

        const data: Disponiblepayload = {
          key: this.key,
          disponible: this.disponible === "oui",
        };

        this.ladda = true;
        this.api.disponibleCoach(data).subscribe(
          res => {
            this.errorMessages = [];
            this.ladda = false;
            console.log('result', res);
          },
          error => {
            console.error('Error', error);
            this.ladda = false;
            this.errorMessages = this.api.flattenErrors(error);
          }
        );
      }
    );
  }

  get debug(): boolean {
    return !environment.production || this.route.snapshot.queryParams.debug === '1';
  }
}
