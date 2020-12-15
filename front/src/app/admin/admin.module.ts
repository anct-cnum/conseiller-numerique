import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AdminRoutingModule } from './admin-routing.module';
import { PageCoachListComponent } from './modules/coach/components/page-coach-list/page-coach-list.component';
import {SharedModule} from 'app/shared/shared.module';
import { AdminLayoutComponent } from './components/admin-layout/admin-layout.component';
import { PageHostListComponent } from './modules/host/components/page-host-list/page-host-list.component';


@NgModule({
  declarations: [PageCoachListComponent, AdminLayoutComponent, PageHostListComponent],
  imports: [
    CommonModule,
    AdminRoutingModule,
    SharedModule,
  ]
})
export class AdminModule { }
