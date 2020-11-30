import {
  api2date,
  api2datetime,
  api2geoPoint,
  date2api, geoPoint2api,
  isDateStruct, isGeoJsonPoint,
  isGeoPoint,
  isStringDate,
  isStringDateTime
} from './utils';
import {isArray, isObject, keysToCamel, keysToSnake} from 'app/utils/utils';
import {DateStruct} from 'app/core/dao/date';
import {GeoPoint} from 'app/core/dao/geo';


export class ApiAdapter {
  static parseDates(obj: any): any {
    if (isStringDateTime(obj)) {
      return api2datetime(obj as string);
    }
    else if (isStringDate(obj)) {
      return api2date(obj as string);
    }
    else if (isArray(obj)) {
      return obj.map(x => this.parseDates(x));
    }
    else if (isObject(obj)) {
      for (const [key, value] of Object.entries(obj)) {
        obj[key] = this.parseDates(value);
      }
    }
    return obj;
  }

  static parseGeo(obj: any): any {
    if (isGeoJsonPoint(obj)) {
      return api2geoPoint(obj);
    }
    else if (isArray(obj)) {
      return obj.map(x => this.parseGeo(x));
    }
    else if (isObject(obj)) {
      for (const [key, value] of Object.entries(obj)) {
        obj[key] = this.parseGeo(value);
      }
    }
    return obj;
  }

  static api2app(json: any): any {
    let obj = keysToCamel(json);
    obj = this.parseDates(obj);
    obj = this.parseGeo(obj);
    return obj;
  }

  static app2api(obj: any): any {
    for (const [key, value] of Object.entries(obj)) {
      if (isDateStruct(value)) {
        obj[key] = date2api(value as DateStruct);
      }
      else if (isGeoPoint(value)) {
        obj[key] = geoPoint2api(value as GeoPoint);
      }
    }
    return keysToSnake(obj);
  }
}
