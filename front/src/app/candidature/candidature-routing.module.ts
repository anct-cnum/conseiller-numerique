import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {PageFormCoachComponent} from './components/page-form-coach/page-form-coach.component';
import {PageFormHostOrganizationComponent} from './components/page-form-host-organization/page-form-host-organization.component';
import {BasePageComponent} from './components/base-page/base-page.component';
import {PageFormCoachSuccessComponent} from './components/page-form-coach-success/page-form-coach-success.component';
import {PageMatchingComponent} from './components/page-matching/page-matching.component';
import {PageFormHostSuccessComponent} from './components/page-form-host-success/page-form-host-success.component';


const routes: Routes = [
  {
    path: '',
    component: BasePageComponent,
    children: [
      {
        path: 'conseiller/new',
        component: PageFormCoachComponent,
      },
      {
        path: 'conseiller/success',
        component: PageFormCoachSuccessComponent,
      },
      {
        path: 'structure/new',
        component: PageFormHostOrganizationComponent,
      },
      {
        path: 'structure/success',
        component: PageFormHostSuccessComponent,
      },
      {
        path: 'conseiller',
        redirectTo: 'conseiller/new',
      },
      {
        path: 'structure',
        redirectTo: 'structure/new',
      },
      {
        path: '',
        redirectTo: 'conseiller',
        pathMatch: 'full',
      },

      {
        path: 'matching/:key/:mode',
        component: PageMatchingComponent,
      },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CandidatureRoutingModule { }
