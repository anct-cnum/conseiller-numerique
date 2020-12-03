import { Injectable } from '@angular/core';
import {FormGroup} from '@angular/forms';
import {ToastrService} from 'ngx-toastr';

@Injectable({
  providedIn: 'root'
})
export class FormUtilsService {

  constructor(
    private toastr: ToastrService,
  ) { }

  preSubmitFormChecks(form: FormGroup): boolean {
    console.log('formValue', form.value);
    form.markAllAsTouched();
    if (!form.valid) {
      window.scroll({top: 0, left: 0, behavior: 'smooth'});
      this.toastr.error('Votre formulaire contient des erreurs');
      console.warn('form is invalid');
      return false;
    }
    return true;
  }

  getInvalidDetails(form: FormGroup): any[] {
    const invalid = [];
    const controls = form.controls;
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
}
