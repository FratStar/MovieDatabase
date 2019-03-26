import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Observable, EMPTY, throwError } from 'rxjs';
import { catchError, retry, map } from 'rxjs/operators';
import {API_URL} from '../env';
import { Movie } from './movie.model'


const httpOptions = {
    headers: new HttpHeaders({
      'Content-Type':  'application/json'
    })
  };

@Injectable({
    providedIn: 'root'
})



export class MovieApiService {
    constructor(private http: HttpClient) {

    }

    searchMovie(title: string, year: string){
      const options = {headers: {'Content-Type': 'application/json'}};
      const url = 'http://www.omdbapi.com/?apikey=e165dea8&t=' + title + '&y=' + year;
      var data = {"Title": title, "Year": year};
      this.http.post<JSON>(`${API_URL}/movie`, JSON.stringify(data), options).subscribe(
        (t:JSON) => console.info(JSON.stringify(t))
      );
      return this.http.get(`${API_URL}/movie`, options)
        .pipe(
          catchError(this.handleError)
            );
    }


    private handleError(error: HttpErrorResponse) {
        if (error.error instanceof ErrorEvent) {
          // A client-side or network error occurred. Handle it accordingly.
          console.error('An error occurred:', error.error.message);
        } else {
          // The backend returned an unsuccessful response code.
          // The response body may contain clues as to what went wrong,
          console.error(
            `Backend returned code ${error.status}, ` +
            `body was: ${error.error}`);
        }
        // return an observable with a user-facing error message
        return throwError(
          'Something bad happened; please try again later.');
      };

    /*  private handleError(error: HttpErrorResponse) {
        let errorMessage = '';
        if (error.error instanceof ErrorEvent) {
          // client-side error
          errorMessage = `Error: ${error.error.message}`;
        } else {
          // server-side error
          errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
        }
        window.alert(errorMessage);
        return throwError(errorMessage);
      }*/

    /*getMovies() {
        return this.http.get<Movie[]>(`${API_URL}/movie`)
            .pipe(
                catchError(this.handleError)
            );
        }
    addMovies(Movie: Movie){
        return this.http.post<Movie>(`${API_URL}/movie`, Movie, httpOptions)
            .pipe(
                catchError(this.handleError)
            );
    }*/
    
}

