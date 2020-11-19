import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';

import { ToastNoAnimationModule } from 'ngx-toastr';


import { LOCALE_ID } from '@angular/core';
import { registerLocaleData } from '@angular/common';
import localeFr from '@angular/common/locales/fr';
import localeFrExtra from '@angular/common/locales/extra/fr';


// the second parameter 'fr' is optional
registerLocaleData(localeFr, 'fr', localeFrExtra);


@NgModule({
  declarations: [],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    // import HttpClientModule after BrowserModule.
    HttpClientModule,
    ToastNoAnimationModule.forRoot(),
  ],
  providers: [
    {provide: LOCALE_ID, useValue: 'fr' },
  ],
})
export class CoreModule { }
