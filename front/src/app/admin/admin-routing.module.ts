import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {PageCoachListComponent} from 'app/admin/coach/components/page-coach-list/page-coach-list.component';

const routes: Routes = [
  {
    path: 'coach/list',
    component: PageCoachListComponent,
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
