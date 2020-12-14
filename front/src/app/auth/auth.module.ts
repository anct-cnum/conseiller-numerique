import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AuthRoutingModule } from './auth-routing.module';
import { PageSignInComponent } from './components/page-sign-in/page-sign-in.component';
import { AuthLayoutComponent } from './components/auth-layout/auth-layout.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {LaddaModule} from 'angular2-ladda';


@NgModule({
  declarations: [PageSignInComponent, AuthLayoutComponent],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    AuthRoutingModule,
    LaddaModule,
  ]
})
export class AuthModule { }
