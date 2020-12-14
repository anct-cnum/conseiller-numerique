import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Observable} from 'rxjs';
import {AuthService} from 'app/core/services/auth.service';


@Component({
  selector: 'app-page-sign-in',
  templateUrl: './page-sign-in.component.html',
  styleUrls: ['./page-sign-in.component.scss']
})
export class PageSignInComponent implements OnInit {

  form: FormGroup;
  ladda$: Observable<boolean>;

  constructor(
    private auth: AuthService,
    private fb: FormBuilder,
  ) {
    this.ladda$ = this.auth.authenticating$;
  }

  ngOnInit(): void {
    this.initForm();
  }

  login(): void {
    if (!this.form.valid) {
      console.log('form invalid');
      return;
    }

    this.auth.authenticate({username: this.form.value.email, password: this.form.value.password}).subscribe(
      _ => {
        console.log('TODO redirect');
      }
    );
  }

  private initForm(): void {
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email, Validators.maxLength(200)]],
      password: ['', [Validators.required, Validators.maxLength(200)]],
    });
  }

}
