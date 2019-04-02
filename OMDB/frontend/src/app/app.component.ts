import { Component,  OnInit, OnDestroy, ViewChild } from '@angular/core';
import { MovieApiService } from './movie/movie-api-service';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  constructor(private movieapiservice: MovieApiService ){}
  
  ngOnInit(){}
}
