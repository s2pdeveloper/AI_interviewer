import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { ConversationService } from '../services/conversation.service';
import { NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {
 result:any;
 id:any;
  constructor(private service: ConversationService, private spinner: NgxSpinnerService) { }

  ngOnInit(): void {
    this.id = localStorage.getItem("id");
    this.viewResult();
  }
  async viewResult(){
    this.spinner.show();
    await this.service.getConvo(this.id).subscribe((data)=>{
      console.log(data);
      this.spinner.hide();
      this.result=data;
    });
  }
  getStars(rating: string): number[] {
    const num = parseInt(rating, 10);
    return Array(num).fill(0); // Return an array with 'num' elements
  }

  // Get the remaining stars needed to make up 5 stars
  getEmptyStars(rating: string): number[] {
    const num = 5 - parseInt(rating, 10);
    return Array(num).fill(0); // Return an array with 'num' elements
  }
  
}
