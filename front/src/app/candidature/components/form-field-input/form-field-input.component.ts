import {Component, Input, OnInit} from '@angular/core';
import {UntypedFormGroup} from '@angular/forms';

@Component({
  selector: 'app-form-field-input',
  templateUrl: './form-field-input.component.html',
  styleUrls: ['./form-field-input.component.scss']
})
export class FormFieldInputComponent implements OnInit {
  @Input()
  form: UntypedFormGroup;

  @Input()
  key: string;

  @Input()
  label: string;

  @Input()
  required: boolean;

  @Input()
  type: string;

  @Input()
  helpText: string;

  constructor() { }

  ngOnInit(): void {
  }

}
