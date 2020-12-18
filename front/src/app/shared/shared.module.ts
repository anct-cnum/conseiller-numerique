import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DateStructPipe } from './pipes/date-struct.pipe';
import {FormErrorBoxComponent} from './forms/form-error-box/form-error-box.component';
import {FormFieldErrorsComponent} from './forms/form-field-errors/form-field-errors.component';
import {FormFieldInputComponent} from './forms/form-field-input/form-field-input.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {NgbModule} from "@ng-bootstrap/ng-bootstrap";
import { IconBooleanComponent } from './table/icon-boolean/icon-boolean.component';
import {MaterialModule} from "app/material/material.module";


@NgModule({
  declarations: [
    FormErrorBoxComponent,
    FormFieldErrorsComponent,
    FormFieldInputComponent,
    DateStructPipe,
    IconBooleanComponent,
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    NgbModule,
    MaterialModule,
  ],
  exports: [
    FormsModule,
    ReactiveFormsModule,
    NgbModule,
    FormErrorBoxComponent,
    FormFieldErrorsComponent,
    FormFieldInputComponent,
    MaterialModule,
    IconBooleanComponent,
  ]
})
export class SharedModule { }
