import { TestBed } from '@angular/core/testing';

import { FormUtilsService } from 'app/core/services/utils/form-utils.service';

describe('FormUtilsService', () => {
  let service: FormUtilsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FormUtilsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
