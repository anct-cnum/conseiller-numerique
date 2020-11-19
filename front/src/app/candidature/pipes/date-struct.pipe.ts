import {Pipe, PipeTransform} from '@angular/core';
import {DatePipe} from '@angular/common';
import {NgbDate} from '@ng-bootstrap/ng-bootstrap';
import {date2api} from '../../core/services/api/utils';


@Pipe({
  name: 'date',
  pure: true,
})
export class DateStructPipe extends DatePipe implements PipeTransform {

  transform(value: any, format = 'mediumDate', timezone?: string, locale?: string): string|null {
    if (value instanceof NgbDate) {
      value = date2api(value);
    }
    return super.transform(value, format, timezone, locale);
  }

}
