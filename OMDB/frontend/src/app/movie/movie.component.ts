import { Movie } from './movie.model';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';

@Component({
  selector: 'app-movie',
  templateUrl: './movie.component.html',
  styleUrls: ['./movie.component.scss']
})
export class MovieComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  movieForm = new FormGroup({
    title: new FormControl(''),
    year : new FormControl(''),
  });

}