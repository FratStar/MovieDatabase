import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { MovieApiService } from './movie-api-service'

@Component({
  selector: 'app-movie',
  templateUrl: './movie.component.html',
  styleUrls: ['./movie.component.scss']
})
export class MovieComponent implements OnInit {

  mov: any;
  title: string;
  year: string;
  
  constructor(private movieapiservice: MovieApiService ){}

  movieForm: FormGroup;

  ngOnInit() {

    this.movieForm = new FormGroup({
      title: new FormControl(''),
      year : new FormControl(''),

    });
  }

  onSubmit()
{
  event.preventDefault();
  //Get User Input
  this.title = this.movieForm.value.title;
  this.year = this.movieForm.value.year;

  this.movieapiservice.searchMovie(this.title, this.year).subscribe(
    (data) => {
      this.mov = data;
      var response = JSON.stringify(data);
     console.log(this.mov.Title);
     console.log(this.mov.Response);
     //console.log(response);
    }
  )
}

search(){
  console.log("hello from search")
}

}