import { Component,  OnInit, OnDestroy, ViewChild } from '@angular/core';
import { Movie } from './movie/movie.model';
import { MovieApiService } from './movie/movie-api-service';
import { FormControl, FormGroup, NgForm } from '@angular/forms';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  private Movies$: Movie[];
  private movies = [];
  mov: any
  title: string;
  year: string;
  constructor(private movieapiservice: MovieApiService ){}

  ngOnInit(){
  }

  movieForm = new FormGroup({
    title: new FormControl(''),
    year : new FormControl(''),
  });

  search(){
    console.log("hello from search")
}
onSubmit(){
  //Get User Input
  this.title = this.movieForm.value.title;
  console.log(this.title);
  this.year = this.movieForm.value.year;
  console.log(this.year);
  
  //
  this.movieapiservice.searchMovie(this.title, this.year).subscribe(
    (data: any) => {
      this.mov = data;
      console.log(this.mov);
    }
  )
}
}
