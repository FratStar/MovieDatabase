import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import {API_URL} from '../env';


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
      var data = {"Title": title, "Year": year};
      this.http.post<JSON>(`${API_URL}/movie`, JSON.stringify(data), options).subscribe(
        (data) => { console.info(data)
        }
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
    
}

