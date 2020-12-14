import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AdminRoutingModule } from './admin-routing.module';
import { PageCoachListComponent } from './coach/components/page-coach-list/page-coach-list.component';


@NgModule({
  declarations: [PageCoachListComponent],
  imports: [
    CommonModule,
    AdminRoutingModule
  ]
})
export class AdminModule { }
