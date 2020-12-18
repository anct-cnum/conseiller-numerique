import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';

import { ToastNoAnimationModule } from 'ngx-toastr';


import { LOCALE_ID } from '@angular/core';
import { registerLocaleData } from '@angular/common';
import localeFr from '@angular/common/locales/fr';
import localeFrExtra from '@angular/common/locales/extra/fr';
import { ErrorInterceptor } from 'app/core/interceptors/error.interceptor';
import { ApiAdapterInterceptor } from 'app/core/interceptors/api-adapter.interceptor';


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
    {provide: HTTP_INTERCEPTORS, useClass: ApiAdapterInterceptor, multi: true},
    {provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true},
  ],
})
export class CoreModule { }
