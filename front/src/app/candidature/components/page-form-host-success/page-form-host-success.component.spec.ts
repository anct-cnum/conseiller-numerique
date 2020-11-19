import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageFormHostSuccessComponent } from './page-form-host-success.component';

describe('PageFormHostSuccessComponent', () => {
  let component: PageFormHostSuccessComponent;
  let fixture: ComponentFixture<PageFormHostSuccessComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PageFormHostSuccessComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PageFormHostSuccessComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
