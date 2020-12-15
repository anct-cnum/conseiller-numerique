import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {PageCoachListComponent} from './modules/coach/components/page-coach-list/page-coach-list.component';
import {AdminLayoutComponent} from './components/admin-layout/admin-layout.component';
import {PageHostListComponent} from './modules/host/components/page-host-list/page-host-list.component';


const routes: Routes = [
  {
    path: '',
    component: AdminLayoutComponent,
    children: [
      {
        path: 'conseillers',
        component: PageCoachListComponent,
      },
      {
        path: 'structures',
        component: PageHostListComponent,
      },
      {
        path: '**',
        redirectTo: 'conseillers',
        pathMatch: 'full',
      }
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
