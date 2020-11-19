import { Component, OnInit } from '@angular/core';
import {ConstantsService} from 'app/core/services/constants.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {
  isNavbarDisplay = false;

  constructor(
    public c: ConstantsService,
  ) { }

  ngOnInit(): void {
  }

}
