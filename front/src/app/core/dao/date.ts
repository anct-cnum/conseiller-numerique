import { NgbDate } from '@ng-bootstrap/ng-bootstrap';
import { NgbDateNativeAdapter } from '@ng-bootstrap/ng-bootstrap';

export class DateStruct extends NgbDate {
  year: number;
  month: number;
  day: number;
}


export function castDate(d: Date|NgbDate) : DateStruct {
  if (!d) {
    return null;
  }
  if (d instanceof Date) {
    let adapter = new NgbDateNativeAdapter();
    let r = adapter.fromModel(d);
    return new DateStruct(r.year, r.month, r.day);
  }
  return d;
}


export function dateEqual(d1: Date|NgbDate, d2: Date|NgbDate) {
  let a = castDate(d1);
  let b = castDate(d2);
  if (!a && !b) {
    return true;
  }
  else if (!a || !b) {
    return false;
  }
  else {
    return a.equals(b);
  }
}


export function dateBefore(d1: Date|NgbDate, d2: Date|NgbDate) {
  let a = castDate(d1);
  let b = castDate(d2);
  if (!a) {
    return false;
  }
  else if (!b) {
    return true;
  }
  else {
    return a.before(b);
  }
}

export function dateBeforeOrEqual(d1: Date|NgbDate, d2: Date|NgbDate) {
  return dateEqual(d1, d2) || dateBefore(d1, d2);
}


export function dateAfter(d1: Date|NgbDate, d2: Date|NgbDate) {
  let a = castDate(d1);
  let b = castDate(d2);
  if (!a) {
    return false;
  }
  else if (!b) {
    return true;
  }
  else {
    return a.after(b);
  }
}

export function dateAfterOrEqual(d1: Date|NgbDate, d2: Date|NgbDate) {
  return dateEqual(d1, d2) || dateAfter(d1, d2);
}
