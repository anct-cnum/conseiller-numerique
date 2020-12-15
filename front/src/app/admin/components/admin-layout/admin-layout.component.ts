import { Component, OnInit } from '@angular/core';
import {ConstantsService} from 'app/core/services/constants.service';
import {Observable} from 'rxjs';
import {AuthService} from 'app/core/services/auth.service';
import {User} from 'app/core/dao/user';

@Component({
  selector: 'app-admin-layout',
  templateUrl: './admin-layout.component.html',
  styleUrls: ['./admin-layout.component.scss']
})
export class AdminLayoutComponent implements OnInit {
  isNavbarDisplay = false;
  loggedInUser$: Observable<User>;

  constructor(
    public c: ConstantsService,
    private auth: AuthService,
  ) {
    this.loggedInUser$ = this.auth.user$;
  }

  ngOnInit(): void {
  }

  logout(): void {
    this.auth.logout('/admin');
  }
}
