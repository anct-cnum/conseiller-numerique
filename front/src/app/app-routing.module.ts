import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

const routes: Routes = [
  {
    path: 'candidature',
    loadChildren: () => import('./candidature/candidature.module').then(m => m.CandidatureModule),
  },
  {
    path: '_internal',
    loadChildren: () => import('./internal/internal.module').then(m => m.InternalModule),
  },
  {
    path: '**',
    redirectTo: '/candidature/conseiller/new',
    pathMatch: 'full',
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
