import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-icon-boolean',
  templateUrl: './icon-boolean.component.html',
  styleUrls: ['./icon-boolean.component.scss']
})
export class IconBooleanComponent implements OnInit {

  @Input() value: boolean;

  constructor() { }

  ngOnInit(): void {
  }

}
