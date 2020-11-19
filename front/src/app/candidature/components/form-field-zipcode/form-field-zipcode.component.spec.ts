import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormFieldZipcodeComponent } from './form-field-zipcode.component';

describe('FormFieldZipcodeComponent', () => {
  let component: FormFieldZipcodeComponent;
  let fixture: ComponentFixture<FormFieldZipcodeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FormFieldZipcodeComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FormFieldZipcodeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
