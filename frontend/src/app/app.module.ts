import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { HelperComponent } from './helper/helper.component';
import { HttpClientModule } from '@angular/common/http';
import { Routes, RouterModule, ROUTES } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { InterviewComponent } from './interview/interview.component';
import { ReactiveFormsModule } from '@angular/forms';
import { ToastrModule } from 'ngx-toastr'

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgxSpinnerModule } from 'ngx-spinner';
import { ResultComponent } from './result/result.component';

const route: Routes = [
  {
    path: '', redirectTo: 'home', pathMatch: 'full'
  },
  {
    path: 'home', component: HomeComponent
  },
  {
    path: 'audio', component: InterviewComponent
  },
  {
    path:'result',component: ResultComponent
  }
]
@NgModule({
  declarations: [
    AppComponent,
    HelperComponent,
    HomeComponent,
    InterviewComponent,
    ResultComponent
  ],
  imports: [
    BrowserModule, HttpClientModule, RouterModule.forRoot(route), ReactiveFormsModule,
    ToastrModule.forRoot(), BrowserAnimationsModule,
    NgxSpinnerModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
