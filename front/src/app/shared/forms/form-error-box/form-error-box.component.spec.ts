import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormErrorBoxComponent } from 'app/shared/forms/form-error-box/form-error-box.component';

describe('FormErrorBoxComponent', () => {
  let component: FormErrorBoxComponent;
  let fixture: ComponentFixture<FormErrorBoxComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FormErrorBoxComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FormErrorBoxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
