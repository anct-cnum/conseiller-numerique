import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {ApiService} from 'app/core/services/api/api.service';
import {ActivatedRoute} from '@angular/router';
import {ToastrService} from 'ngx-toastr';
import {FormUtilsService} from 'app/core/services/utils/form-utils.service';
import {environment} from '@env';
import {Unsubscribepayload} from 'app/core/dao/unsubscribepayload';

@Component({
  selector: 'app-page-host-unsubscribe',
  templateUrl: './page-host-unsubscribe.component.html',
  styleUrls: ['./page-host-unsubscribe.component.scss']
})
export class PageHostUnsubscribeComponent implements OnInit {

  form: FormGroup;
  errorMessages: string[];
  ladda: boolean;
  isConfirmed: boolean;
  key: string;

  constructor(
    private api: ApiService,
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private toast: ToastrService,
    public formUtils: FormUtilsService,
  ) { }

  ngOnInit(): void {
    this.errorMessages = [];
    this.ladda = false;
    this.isConfirmed = false;
    this.form = this.formBuilder.group({
      reason: [null, Validators.required],
    });
    this.route.params.subscribe(
      params => {
        this.key = params.key || null;
      }
    );
  }

  get debug(): boolean {
    return !environment.production || this.route.snapshot.queryParams.debug === '1';
  }

  onSubmit(): void {
    if (!this.formUtils.preSubmitFormChecks(this.form)) {
      return;
    }

    const data: Unsubscribepayload = {
      key: this.key,
      extras: {
        reason: this.form.value.reason,
      },
    };

    this.ladda = true;
    this.api.unsubscribeHostOrganization(data).subscribe(
      res => {
        this.errorMessages = [];
        this.ladda = false;
        this.isConfirmed = true;
        console.log('result', res);
      },
      error => {
        console.error('Error', error);
        this.ladda = false;
        this.errorMessages = this.api.flattenErrors(error);
      }
    );
  }
}
