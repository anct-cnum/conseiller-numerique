import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {PageBootstrapComponent} from './components/page-bootstrap/page-bootstrap.component';


const routes: Routes = [
  {
    path: 'bootstrap',
    component: PageBootstrapComponent,
  },
  {
    path: '',
    redirectTo: 'bootstrap',
    pathMatch: 'full',
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class InternalRoutingModule { }
