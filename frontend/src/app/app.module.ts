import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { HelperComponent } from './helper/helper.component';
import { HttpClientModule } from '@angular/common/http';
import { Routes, RouterModule, ROUTES } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { InterviewComponent } from './interview/interview.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ToastrModule } from 'ngx-toastr'

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgxSpinnerModule } from 'ngx-spinner';
import { ResultComponent } from './result/result.component';
import { InterrogationComponent } from './interrogation/interrogation.component';

const route: Routes = [
  {
    path: '', redirectTo: 'interrogation', pathMatch: 'full'
  },
  {
    path: 'home', component: HomeComponent
  },
  {
    path: 'audio', component: InterviewComponent
  },
  {
    path:'result',component: ResultComponent
  },
  {
    path:'interrogation',component: InterrogationComponent
  }
]
@NgModule({
  declarations: [
    AppComponent,
    HelperComponent,
    HomeComponent,
    InterviewComponent,
    ResultComponent,
    InterrogationComponent
  ],
  imports: [
    BrowserModule, HttpClientModule, RouterModule.forRoot(route), ReactiveFormsModule,
    ToastrModule.forRoot(), BrowserAnimationsModule,
    NgxSpinnerModule,FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
