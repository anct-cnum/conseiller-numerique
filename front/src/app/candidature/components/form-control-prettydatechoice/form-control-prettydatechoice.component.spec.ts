import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormControlPrettyDateChoiceComponent } from './form-control-prettydatechoice.component';

describe('FormControlPrettydatechoiceComponent', () => {
  let component: FormControlPrettyDateChoiceComponent;
  let fixture: ComponentFixture<FormControlPrettyDateChoiceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FormControlPrettyDateChoiceComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FormControlPrettyDateChoiceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
