import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageFormCoachComponent } from './page-form-coach.component';

describe('FormCoachComponent', () => {
  let component: PageFormCoachComponent;
  let fixture: ComponentFixture<PageFormCoachComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PageFormCoachComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PageFormCoachComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
