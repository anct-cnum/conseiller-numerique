import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormFieldErrorsComponent } from 'app/shared/forms/form-field-errors/form-field-errors.component';

describe('FormFieldErrorsComponent', () => {
  let component: FormFieldErrorsComponent;
  let fixture: ComponentFixture<FormFieldErrorsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FormFieldErrorsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FormFieldErrorsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
