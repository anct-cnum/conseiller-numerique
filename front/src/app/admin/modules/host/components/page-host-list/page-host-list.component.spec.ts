import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageHostListComponent } from 'app/admin/modules/host/components/page-host-list/page-host-list.component';

describe('PageHostListComponent', () => {
  let component: PageHostListComponent;
  let fixture: ComponentFixture<PageHostListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PageHostListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PageHostListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
