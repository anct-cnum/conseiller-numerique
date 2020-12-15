import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Observable} from 'rxjs';
import {AuthService} from 'app/core/services/auth.service';
import {ApiService} from "app/core/services/api/api.service";
import {ActivatedRoute, Router} from "@angular/router";


@Component({
  selector: 'app-page-sign-in',
  templateUrl: './page-sign-in.component.html',
  styleUrls: ['./page-sign-in.component.scss']
})
export class PageSignInComponent implements OnInit {

  form: FormGroup;
  ladda$: Observable<boolean>;
  errorMessages: string[];
  next: string;

  constructor(
    private auth: AuthService,
    private api: ApiService,
    private fb: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
  ) {
    this.ladda$ = this.auth.authenticating$;
  }

  ngOnInit(): void {
    this.initForm();
    this.route.queryParams.subscribe(
      params => {
        this.next = params.next || '';
      }
    );
  }

  login(): void {
    if (!this.form.valid) {
      console.log('form invalid');
      return;
    }

    this.auth.authenticate({username: this.form.value.email, password: this.form.value.password}).subscribe(
      _ => {
        this.router.navigateByUrl(this.next);
      },
      err => {
        if (err.status === 401) {
          this.errorMessages = ['Échec de l\'identification'];
        }
        else {
          this.errorMessages = this.api.flattenErrors(err);
        }
      },
    );
  }

  private initForm(): void {
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email, Validators.maxLength(200)]],
      password: ['', [Validators.required, Validators.maxLength(200)]],
    });
  }

}
