import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageFormHostOrganizationComponent } from './page-form-host-organization.component';

describe('FormHostingOrganizationComponent', () => {
  let component: PageFormHostOrganizationComponent;
  let fixture: ComponentFixture<PageFormHostOrganizationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PageFormHostOrganizationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PageFormHostOrganizationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
