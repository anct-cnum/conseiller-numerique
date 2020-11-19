import {api2date, api2datetime, date2api, isDateStruct, isStringDate, isStringDateTime} from './utils';
import {isArray, isObject, keysToCamel, keysToSnake} from 'app/utils/utils';
import {DateStruct} from 'app/core/dao/date';


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

  static api2app(json: any): any {
    let obj = keysToCamel(json);
    obj = this.parseDates(obj);
    return obj;
  }

  static app2api(obj: any): any {
    for (const [key, value] of Object.entries(obj)) {
      if (isDateStruct(value)) {
        obj[key] = date2api(value as DateStruct);
      }
    }
    return keysToSnake(obj);
  }
}
