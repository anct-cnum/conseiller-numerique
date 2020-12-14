import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageCoachListComponent } from './page-coach-list.component';

describe('PageCoachListComponent', () => {
  let component: PageCoachListComponent;
  let fixture: ComponentFixture<PageCoachListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PageCoachListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PageCoachListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
