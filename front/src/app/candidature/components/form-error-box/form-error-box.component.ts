import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-form-error-box',
  templateUrl: './form-error-box.component.html',
  styleUrls: ['./form-error-box.component.scss']
})
export class FormErrorBoxComponent implements OnInit {

  @Input() errorMessages: string[];

  constructor() { }

  ngOnInit(): void {
  }

}
