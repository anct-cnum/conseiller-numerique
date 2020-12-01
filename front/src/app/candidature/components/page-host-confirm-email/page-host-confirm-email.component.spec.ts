import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageHostConfirmEmailComponent } from './page-host-confirm-email.component';

describe('PageHostConfirmEmailComponent', () => {
  let component: PageHostConfirmEmailComponent;
  let fixture: ComponentFixture<PageHostConfirmEmailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PageHostConfirmEmailComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PageHostConfirmEmailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
