import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageHostUnsubscribeComponent } from './page-host-unsubscribe.component';

describe('PageHostUnsubscribeComponent', () => {
  let component: PageHostUnsubscribeComponent;
  let fixture: ComponentFixture<PageHostUnsubscribeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PageHostUnsubscribeComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PageHostUnsubscribeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
