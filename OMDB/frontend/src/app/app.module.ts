import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {HttpClientModule} from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { navbar } from './navbar';
import { MovieApiService } from './movie/movie-api-service';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { MovieComponent } from './movie/movie.component';



@NgModule({
  declarations: [
    AppComponent,
    navbar
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule
  ],
  providers: [MovieApiService], 
  bootstrap: [AppComponent]
})
export class AppModule { }
