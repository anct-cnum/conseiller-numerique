import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageCoachUnsubscribeComponent } from './page-coach-unsubscribe.component';

describe('PageCoachUnsubscribeComponent', () => {
  let component: PageCoachUnsubscribeComponent;
  let fixture: ComponentFixture<PageCoachUnsubscribeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PageCoachUnsubscribeComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PageCoachUnsubscribeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
