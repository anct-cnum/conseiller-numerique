import { Component, OnInit } from '@angular/core';
import { NgbCalendar } from '@ng-bootstrap/ng-bootstrap';
import {AbstractControl, FormBuilder, FormGroup, ValidatorFn, Validators} from '@angular/forms';
import {CoachInput} from 'app/core/dao/coach';
import {ApiService} from 'app/core/services/api/api.service';
import {isArray} from 'app/utils/utils';
import {ActivatedRoute, Router} from '@angular/router';
import {environment} from '@env';
import {ToastrService} from 'ngx-toastr';
import {OptionCommune} from '../form-field-zipcode/form-field-zipcode.component';


function requiredIfFieldTrue(otherFieldName: string): ValidatorFn {
  return (control: AbstractControl): {[key: string]: any} | null => {
    if (control.parent?.get(otherFieldName)?.value) {
      return Validators.required(control);
    }
  };
}


function atLeastOne(group: FormGroup): {[key: string]: any} | null {
  for (const control of Object.values(group.controls)) {
    if (control.value) {
      return null;
    }
  }
  return { required: true };
}


export function phoneValidator(control: AbstractControl): {[key: string]: any} | null {
  let s: string = control?.value ?? '';
  s = s.replace(/ /g, '');
  if ('' === s || /[0-9]{10}/.test(s)) {
    return null;
  }
  else {
    return { phone: true };
  }
}



@Component({
  selector: 'app-form-coach',
  templateUrl: './page-form-coach.component.html',
  styleUrls: ['./page-form-coach.component.scss']
})
export class PageFormCoachComponent implements OnInit {

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
  ) { }

  ngOnInit(): void {
    this.errorMessages = [];
    this.ladda = false;
    this.form = this.formBuilder.group({
      situation: this.formBuilder.group({
        looking: [false],
        job: [false],
        learning: [false],
        graduated: [false],
      }, {validators: [atLeastOne]}),
      formation: ['', requiredIfFieldTrue('situation.graduated')],
      hasExperience: [null, Validators.required],
      startDate: [null, Validators.required],
      zipCode: ['', Validators.required],
      maxDistance: [0, Validators.required],
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      phone: ['', phoneValidator],
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

    const resource: CoachInput = {
      situationLooking: this.form.value.situation.looking,
      situationJob: this.form.value.situation.job,
      situationLearning: this.form.value.situation.learning,
      situationGraduated: this.form.value.situation.graduated,
      formation: this.form.value.formation,
      hasExperience: this.form.value.hasExperience,
      startDate: this.form.value.startDate.date,
      maxDistance: this.form.value.maxDistance,
      firstName: this.form.value.firstName,
      lastName: this.form.value.lastName,
      email: this.form.value.email,
      phone: this.form.value.phone,
      recaptcha: this.form.value.recaptcha,

      geoName: optionCommune.commune.name,
      zipCode: optionCommune.zipCode,
      communeCode: optionCommune.commune.code,
      departementCode: optionCommune.commune.departementCode,
      regionCode: optionCommune.commune.regionCode,
      location: optionCommune.commune.center,
    };

    this.ladda = true;
    this.api.postCoachApplication(resource).subscribe(
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
        console.error('Error', error);
      }
    );
  }

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

  get debug(): boolean {
    return !environment.production || this.route.snapshot.queryParams.debug === '1';
  }
}
