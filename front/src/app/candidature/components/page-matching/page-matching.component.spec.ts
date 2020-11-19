import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageMatchingComponent } from './page-matching.component';

describe('MatchingComponent', () => {
  let component: PageMatchingComponent;
  let fixture: ComponentFixture<PageMatchingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PageMatchingComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PageMatchingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
