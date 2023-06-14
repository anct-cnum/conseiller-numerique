import {Pipe, PipeTransform} from '@angular/core';
import {DatePipe} from '@angular/common';
import {date2api, isDateStruct} from 'app/core/services/api/utils';


@Pipe({
  name: 'date',
  pure: true,
})
export class DateStructPipe extends DatePipe implements PipeTransform {

  // @ts-ignore
  transform(value: string | number | Date, format: string = 'mediumDate', timezone?: string, locale?: string): string {
    if (isDateStruct(value)) {
      // @ts-ignore
      value = date2api(value);
    }
    // @ts-ignore
    return super.transform(value, format, timezone, locale);
  }

}
