import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PageBootstrapComponent } from './components/page-bootstrap/page-bootstrap.component';
import {InternalRoutingModule} from "./internal-routing.module";



@NgModule({
  declarations: [
    PageBootstrapComponent,
  ],
  imports: [
    CommonModule,
    InternalRoutingModule,
  ]
})
export class InternalModule { }
