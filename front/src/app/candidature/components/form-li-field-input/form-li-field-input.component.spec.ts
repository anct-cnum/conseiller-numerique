import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormLiFieldInputComponent } from 'app/candidature/components/form-li-field-input/form-li-field-input.component';

describe('FormFieldTextComponent', () => {
  let component: FormLiFieldInputComponent;
  let fixture: ComponentFixture<FormLiFieldInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FormLiFieldInputComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FormLiFieldInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
