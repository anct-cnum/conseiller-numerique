import {Component, Input, OnInit} from '@angular/core';
import {FormFieldInputComponent} from 'app/shared/forms/form-field-input/form-field-input.component';


@Component({
  selector: 'app-li-form-field-input',
  templateUrl: './form-li-field-input.component.html',
  styleUrls: ['./form-li-field-input.component.scss']
})
export class FormLiFieldInputComponent extends FormFieldInputComponent {
}
