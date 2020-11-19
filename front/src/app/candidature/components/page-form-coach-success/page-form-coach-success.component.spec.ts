import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageFormCoachSuccessComponent } from './page-form-coach-success.component';

describe('PageFormCoachSuccessComponent', () => {
  let component: PageFormCoachSuccessComponent;
  let fixture: ComponentFixture<PageFormCoachSuccessComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PageFormCoachSuccessComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PageFormCoachSuccessComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
