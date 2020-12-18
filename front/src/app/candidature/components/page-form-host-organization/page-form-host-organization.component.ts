import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {NgbCalendar} from '@ng-bootstrap/ng-bootstrap';
import {ApiService} from 'app/core/services/api/api.service';
import {ActivatedRoute, Router} from '@angular/router';
import {environment} from '@env';
import {HostOrganizationInput} from 'app/core/dao/hostorganization';
import {isArray} from 'app/utils/utils';
import {phoneValidator} from '../page-form-coach/page-form-coach.component';
import {ToastrService} from 'ngx-toastr';
import {OptionCommune} from '../form-field-zipcode/form-field-zipcode.component';
import {FormUtilsService} from 'app/core/services/utils/form-utils.service';


@Component({
  selector: 'app-form-host-organization',
  templateUrl: './page-form-host-organization.component.html',
  styleUrls: ['./page-form-host-organization.component.scss']
})
export class PageFormHostOrganizationComponent implements OnInit {

  form: FormGroup;
  errorMessages: string[];
  ladda: boolean;

  constructor(
    private calendar: NgbCalendar,
    private formBuilder: FormBuilder,
    private api: ApiService,
    private router: Router,
    private route: ActivatedRoute,
    private toast: ToastrService,
    public formUtils: FormUtilsService,
  ) {}

  ngOnInit(): void {
    this.errorMessages = [];
    this.ladda = false;
    this.form = this.formBuilder.group({
      type: [null, Validators.required],
      hasCandidate: [null, Validators.required],
      zipCode: [null, Validators.required],
      startDate: [null, Validators.required],
      name: ['', Validators.required],
      contactFirstName: ['', Validators.required],
      contactLastName: ['', Validators.required],
      contactJob: ['', Validators.required],
      contactEmail: ['', [Validators.required, Validators.email]],
      contactPhone: ['', phoneValidator],
      checkboxConfirm: [false, Validators.requiredTrue],
      recaptcha: [null, Validators.required],
    });
  }

  onSubmit(): void {
    if (!this.formUtils.preSubmitFormChecks(this.form)) {
      return;
    }

    const resource = this._generateHostOrganizationInput();

    this.ladda = true;
    this.api.postHostingOrganizationApplication(resource).subscribe(
      application => {
        this.errorMessages = [];
        this.ladda = false;
        console.log('result', application);
        this.router.navigate(['..', 'success'], {relativeTo: this.route});
      },
      error => {
        console.error('Error', error);
        this.errorMessages = this.api.flattenErrors(error);
        this.ladda = false;
      }
    );
  }

  private _generateHostOrganizationInput(): HostOrganizationInput {
    const optionCommune: OptionCommune = this.form.value.zipCode;
    return {
      type: this.form.value.type,
      hasCandidate: this.form.value.hasCandidate,
      startDate: this.form.value.startDate.date,
      name: this.form.value.name,
      contactJob: this.form.value.contactJob,
      contactFirstName: this.form.value.contactFirstName,
      contactLastName: this.form.value.contactLastName,
      contactEmail: this.form.value.contactEmail,
      contactPhone: this.form.value.contactPhone,
      recaptcha: this.form.value.recaptcha,

      geoName: optionCommune.commune.name,
      zipCode: optionCommune.zipCode,
      communeCode: optionCommune.commune.code,
      departementCode: optionCommune.commune.departementCode,
      regionCode: optionCommune.commune.regionCode,
      location: optionCommune.commune.center,
    };
  }

  // TODO refactor with page-coach-form
  get debug(): boolean {
    return !environment.production || this.route.snapshot.queryParams.debug === '1';
  }

}
