import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {AuthGuard} from 'app/core/guards/auth.guard';

const routes: Routes = [
  {
    path: 'candidature',
    loadChildren: () => import('./candidature/candidature.module').then(m => m.CandidatureModule),
  },
  {
    path: 'admin',
    canActivate: [AuthGuard],
    canActivateChild: [AuthGuard],
    loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule),
  },
  {
    path: 'auth',
    loadChildren: () => import('./auth/auth.module').then(m => m.AuthModule),
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
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
