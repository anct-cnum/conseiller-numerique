import { Component, OnInit } from '@angular/core';
import {ApiService} from 'app/core/services/api/api.service';
import {UntypedFormBuilder, UntypedFormGroup, Validators} from '@angular/forms';
import {environment} from '@env';
import {ActivatedRoute} from '@angular/router';
import {ToastrService} from 'ngx-toastr';
import {Unsubscribepayload} from 'app/core/dao/unsubscribepayload';
import {FormUtilsService} from 'app/core/services/utils/form-utils.service';


@Component({
  selector: 'app-page-coach-unsubscribe',
  templateUrl: './page-coach-unsubscribe.component.html',
  styleUrls: ['./page-coach-unsubscribe.component.scss']
})
export class PageCoachUnsubscribeComponent implements OnInit {

  form: UntypedFormGroup;
  errorMessages: string[];
  ladda: boolean;
  isConfirmed: boolean;
  key: string;

  constructor(
    private api: ApiService,
    private formBuilder: UntypedFormBuilder,
    private route: ActivatedRoute,
    private toast: ToastrService,
    public formUtils: FormUtilsService,
  ) { }

  ngOnInit(): void {
    this.errorMessages = [];
    this.ladda = false;
    this.isConfirmed = false;
    this.form = this.formBuilder.group({
      isUseful: [null, Validators.required],
      comment: [''],
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
        isUseful: this.form.value.isUseful,
        comment: this.form.value.comment,
      },
    };

    this.ladda = true;
    this.api.unsubscribeCoach(data).subscribe(
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
