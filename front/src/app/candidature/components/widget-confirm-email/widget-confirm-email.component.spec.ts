import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WidgetConfirmEmailComponent } from './widget-confirm-email.component';

describe('WidgetConfirmEmailComponent', () => {
  let component: WidgetConfirmEmailComponent;
  let fixture: ComponentFixture<WidgetConfirmEmailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WidgetConfirmEmailComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WidgetConfirmEmailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
