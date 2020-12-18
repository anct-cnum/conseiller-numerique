import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IconBooleanComponent } from './icon-boolean.component';

describe('IconBooleanComponent', () => {
  let component: IconBooleanComponent;
  let fixture: ComponentFixture<IconBooleanComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ IconBooleanComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(IconBooleanComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
