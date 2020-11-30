import { DateStruct } from 'app/core/dao/date';
import { padNumber, isString, isObject } from 'app/utils/utils';
import {GeoPoint, GeoJsonPoint} from "../../dao/geo";
import {RawConfigFile} from "tslint/lib/configuration";


/**
 * Return date formatted as string "yyyy-mm-dd".
 */
export function date2api(date: Date|DateStruct) : string {
  if (!date) {
    return undefined;
  }
  if (date instanceof Date) {
    return '' + date.getFullYear() + '-' + (''+(date.getMonth()+1)).padStart(2, '0') + '-' + (''+date.getDate()).padStart(2, '0');
  }
  else {
    return '' + date.year + '-' + padNumber(date.month) + '-' + padNumber(date.day);
  }
}


/**
 * s: yyyy-mm-dd
 */
export function api2date(s: string) : DateStruct {
  const re = /([0-9]{4})-([0-9]{2})-([0-9]{2})/;

  if (!s) {
    return null;
  }
  let t = re.exec(s);
  if (t) {
    return new DateStruct(parseInt(t[1]), parseInt(t[2]), parseInt(t[3]));
  }
  return null;
}


export function datetime2api(date: Date) : string {
  return date.toISOString();
}

export function api2datetime(s: string) : Date {
  return new Date(s);
}


export function isStringDateTime(s: any) : boolean {
  if (!isString(s)) {
    return false;
  }
  const r = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.?\d*Z$/;
  return r.test(s);
}


export function isStringDate(s: any) : boolean {
  if (!isString(s)) {
    return false;
  }
  const r = /^\d{4}-\d{2}-\d{2}$/;
  return r.test(s);
}


export function isDateStruct(o: any) : boolean {
  // be sure to exclude undefined and null because isObject(null | undefined) returns true
  if (!o || !isObject(o) || o instanceof Date) {
    return false;
  }
  let keys = new Set(Object.keys(o));
  return keys.has('year') && keys.has('month') && keys.has('day');
}


export function isGeoJsonPoint(o: any): boolean {
  return o?.type === 'Point';
}


export function isGeoPoint(o: any): boolean {
  return o && o.hasOwnProperty('longitude')  && o.hasOwnProperty('latitude');
}


export function api2geoPoint(o: any): GeoPoint {
  return {
    longitude: o.coordinates[0],
    latitude: o.coordinates[1],
  };
}


export function geoPoint2api(o: GeoPoint): GeoJsonPoint {
  return {
    type: 'Point',
    coordinates: [o.longitude, o.latitude],
  };
}
