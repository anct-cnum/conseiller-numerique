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
    console.log('formValue', this.form.value);
    this.form.markAllAsTouched();
    if (!this.form.valid) {
      window.scroll({top: 0, left: 0, behavior: 'smooth'});
      this.toast.error('Votre formulaire contient des erreurs');
      console.warn('form is invalid');
      return;
    }

    const optionCommune: OptionCommune = this.form.value.zipCode;
    const resource: HostOrganizationInput = {
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

    this.ladda = true;
    this.api.postHostingOrganizationApplication(resource).subscribe(
      application => {
        this.errorMessages = [];
        this.ladda = false;
        console.log('result', application);
        this.router.navigate(['..', 'success'], {relativeTo: this.route});
      },
      error => {
        this.errorMessages = [];
        this.ladda = false;
        for (const [key, value] of Object.entries(error.error)) {
          let prefix = key + ' : ';
          if (key === 'non_field_errors') {
            prefix = '';
          }
          if (isArray(value)) {
            for (const msg of (value as any[])) {
              this.errorMessages.push(prefix + msg);
            }
          }
          else {
            this.errorMessages.push(prefix + value);
          }
        }
        console.error(error);
      }
    );
  }

  // TODO refactor with page-coach-form
  getInvalidDetails(): any[] {
    const invalid = [];
    const controls = this.form.controls;
    for (const name in controls) {
      if (controls[name].invalid) {
        invalid.push({
          name,
          errors: controls[name].errors,
        });
      }
    }
    return invalid;
  }

  // TODO refactor with page-coach-form
  get debug(): boolean {
    return !environment.production || this.route.snapshot.queryParams.debug === '1';
  }

}
