import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PageFormCoachComponent } from './components/page-form-coach/page-form-coach.component';
import { PageFormHostOrganizationComponent } from './components/page-form-host-organization/page-form-host-organization.component';
import { CandidatureRoutingModule } from './candidature-routing.module';
import { BasePageComponent } from './components/base-page/base-page.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { LaddaModule } from 'angular2-ladda';
import { PageFormCoachSuccessComponent } from './components/page-form-coach-success/page-form-coach-success.component';
import { FormLiFieldInputComponent } from 'app/candidature/components/form-li-field-input/form-li-field-input.component';
import { PageMatchingComponent } from './components/page-matching/page-matching.component';
import { FormSuccessComponent } from './components/form-success/form-success.component';
import { PageFormHostSuccessComponent } from './components/page-form-host-success/page-form-host-success.component';
import {NgSelectModule} from '@ng-select/ng-select';
import { FormFieldZipcodeComponent } from './components/form-field-zipcode/form-field-zipcode.component';
import { FormControlPrettyDateChoiceComponent } from './components/form-control-prettydatechoice/form-control-prettydatechoice.component';
import { FooterComponent } from './components/footer/footer.component';
import {
  RecaptchaModule,
  RecaptchaFormsModule,
  RECAPTCHA_SETTINGS,
  RecaptchaSettings,
  RECAPTCHA_LANGUAGE
} from 'ng-recaptcha';
import {environment} from '@env';
import { SharedModule } from 'app/shared/shared.module';
import { PageCoachConfirmEmailComponent } from './components/page-coach-confirm-email/page-coach-confirm-email.component';
import { PageHostConfirmEmailComponent } from './components/page-host-confirm-email/page-host-confirm-email.component';
import { WidgetConfirmEmailComponent } from './components/widget-confirm-email/widget-confirm-email.component';
import { PageHostUnsubscribeComponent } from './components/page-host-unsubscribe/page-host-unsubscribe.component';
import { PageCoachUnsubscribeComponent } from './components/page-coach-unsubscribe/page-coach-unsubscribe.component';


@NgModule({
  declarations: [
    PageFormCoachComponent,
    PageFormHostOrganizationComponent,
    BasePageComponent,
    NavbarComponent,
    PageFormCoachSuccessComponent,
    FormLiFieldInputComponent,
    PageMatchingComponent,
    FormSuccessComponent,
    PageFormHostSuccessComponent,
    FormFieldZipcodeComponent,
    FormControlPrettyDateChoiceComponent,
    FooterComponent,
    PageCoachConfirmEmailComponent,
    PageHostConfirmEmailComponent,
    WidgetConfirmEmailComponent,
    PageHostUnsubscribeComponent,
    PageCoachUnsubscribeComponent,
  ],

  imports: [
    CommonModule,
    NgSelectModule,
    CandidatureRoutingModule,
    LaddaModule,
    RecaptchaModule,
    RecaptchaFormsModule,
    SharedModule,
  ],

  providers: [
    {
      provide: RECAPTCHA_SETTINGS,
      useValue: { siteKey: environment.reCaptachaSiteKey } as RecaptchaSettings,
    },
    {
      provide: RECAPTCHA_LANGUAGE,
      useValue: 'fr',
    },
  ],

})
export class CandidatureModule { }
