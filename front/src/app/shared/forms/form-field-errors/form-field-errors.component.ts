import {Component, Input, OnInit} from '@angular/core';
import {AbstractControl} from '@angular/forms';

@Component({
  selector: 'app-form-field-errors',
  templateUrl: './form-field-errors.component.html',
  styleUrls: ['./form-field-errors.component.scss']
})
export class FormFieldErrorsComponent implements OnInit {
  @Input() field: AbstractControl;

  constructor() { }

  ngOnInit(): void {
  }

  showError(): boolean {
    return this.field.invalid && (this.field.dirty || this.field.touched);
  }

}
