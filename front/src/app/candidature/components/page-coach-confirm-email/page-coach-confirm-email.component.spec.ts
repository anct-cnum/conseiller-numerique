import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageCoachConfirmEmailComponent } from './page-coach-confirm-email.component';

describe('PageCoachConfirmEmailComponent', () => {
  let component: PageCoachConfirmEmailComponent;
  let fixture: ComponentFixture<PageCoachConfirmEmailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PageCoachConfirmEmailComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PageCoachConfirmEmailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
