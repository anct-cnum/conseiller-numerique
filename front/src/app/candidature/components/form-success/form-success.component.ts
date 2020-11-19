import {Component, Input, OnInit} from '@angular/core';
import {ConstantsService} from 'app/core/services/constants.service';

@Component({
  selector: 'app-form-success',
  templateUrl: './form-success.component.html',
  styleUrls: ['./form-success.component.scss']
})
export class FormSuccessComponent implements OnInit {
  @Input() personOfInterest: string;

  constructor(
    public c: ConstantsService,
  ) { }

  ngOnInit(): void {
  }

}
