import { Injectable } from '@angular/core';
import {UntypedFormGroup} from '@angular/forms';
import {ToastrService} from 'ngx-toastr';

@Injectable({
  providedIn: 'root'
})
export class FormUtilsService {

  constructor(
    private toastr: ToastrService,
  ) { }

  preSubmitFormChecks(form: UntypedFormGroup): boolean {
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

  getInvalidDetails(form: UntypedFormGroup): any[] {
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
