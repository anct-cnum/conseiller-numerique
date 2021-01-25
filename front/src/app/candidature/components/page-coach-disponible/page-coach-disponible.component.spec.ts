import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageCoachDisponibleComponent } from './page-coach-disponible.component';

describe('PageCoachUnsubscribeComponent', () => {
  let component: PageCoachDisponibleComponent;
  let fixture: ComponentFixture<PageCoachDisponibleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PageCoachDisponibleComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PageCoachDisponibleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
