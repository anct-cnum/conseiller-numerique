import {Component, forwardRef, Input, OnInit, Output} from '@angular/core';
import {ControlValueAccessor, NG_VALUE_ACCESSOR} from '@angular/forms';
import {NgbCalendar, NgbDateStruct} from '@ng-bootstrap/ng-bootstrap';


export interface FormControlPrettyDateChoiceValue {
  key: string;
  date: NgbDateStruct;
}

@Component({
  selector: 'app-form-control-prettydatechoice',
  templateUrl: './form-control-prettydatechoice.component.html',
  styleUrls: ['./form-control-prettydatechoice.component.scss'],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => FormControlPrettyDateChoiceComponent),
      multi: true
    },
  ],
})
export class FormControlPrettyDateChoiceComponent implements OnInit, ControlValueAccessor {

  set value(val: FormControlPrettyDateChoiceValue) {
    this.valueKey = val?.key;
    this.valueDate = val?.date;
    this.notify();
  }

  get value(): FormControlPrettyDateChoiceValue {
    if (!this.valueDate) {
      return null;
    }
    return {
      key: this.valueKey,
      date: this.valueDate,
    };
  }

  valueKey: string;
  valueDate: NgbDateStruct;
  options;

  set key(val: string) {
    this.valueKey = val;
    this.valueDate = this.computeDateFromKey(val);
    this.notify();
  }

  get key(): string {
    return this.valueKey;
  }

  set date(val: NgbDateStruct) {
    this.valueDate = val;
    this.notify();
  }

  get date(): NgbDateStruct {
    return this.valueDate;
  }

  onChange: any = () => {};
  onTouched: any = () => {};

  constructor(
    private calendar: NgbCalendar,
  ) {}

  ngOnInit(): void {
    this.valueKey = null;
    this.valueDate = null;
    this.options = [
      {
        key: 'tomorrow',
        label: 'Demain',
      },
      {
        key: 'week1',
        label: 'La semaine prochaine',
      },
      {
        key: 'week2',
        label: 'Dans deux semaines',
      },
      {
        key: 'month1',
        label: 'Dans un mois',
      },
      {
        key: 'month3',
        label: 'Dans trois mois',
      },
      {
        key: 'other',
        label: 'Autre',
      },
    ];
  }

  // ================================
  // ValueAccessor implementation
  // ================================

  // this method sets the value programmatically
  writeValue(value: any): void {
    this.value = value;
  }

  // upon UI element value changes, this method gets triggered
  registerOnChange(fn: any): void {
    this.onChange = fn;
  }

  // upon touching the element, this method gets triggered
  registerOnTouched(fn: any): void {
    this.onTouched = fn;
  }

  setDisabledState(isDisabled: boolean): void {
  }

  // ================================
  // END ValueAccessor implementation
  // ================================

  notify(): void {
    this.onChange(this.value);
    this.onTouched();
  }

  computeDateFromKey(key: string): NgbDateStruct {
    const today = this.calendar.getToday();
    switch (key) {
      case 'tomorrow':
        return this.calendar.getNext(today, 'd', 1);
      case 'week1':
        return this.calendar.getNext(today, 'd', 7);
      case 'week2':
        return this.calendar.getNext(today, 'd', 14);
      case 'month1':
        return this.calendar.getNext(today, 'm', 1);
      case 'month3':
        return this.calendar.getNext(today, 'm', 3);
      case 'other':
        return today;
    }
    return null;
  }
}
