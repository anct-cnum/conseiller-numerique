import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {AuthLayoutComponent} from 'app/auth/components/auth-layout/auth-layout.component';
import {PageSignInComponent} from 'app/auth/components/page-sign-in/page-sign-in.component';


const routes: Routes = [
  {
    path: '',
    component: AuthLayoutComponent,
    children: [
      {path: 'login', component: PageSignInComponent},
    ],
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AuthRoutingModule { }
