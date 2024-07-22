import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { ConversationService } from '../services/conversation.service';
import { NgxSpinnerService } from 'ngx-spinner';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})

export class HomeComponent implements OnInit {

  constructor(private route: Router,
    private toastr: ToastrService,
    private service: ConversationService,
    private spinner: NgxSpinnerService
  ) { }

  ngOnInit(): void {
  }
  reactiveForm = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email])
  })

  loaded:boolean=true;
  submit() {
    //this.loaded=false;
    this.spinner.show();
    if (this.reactiveForm.invalid) {
      //alert('kkk')
      this.toastr.error('valid email id is required')
      return
    }

    let payload = {
      email: this.reactiveForm.value.email,
      uniqueId: Date.now()
    }
    //console.log(this.obj);
    //this.service.createConvo()
    this.service.createConvo(payload).subscribe((res) => {

      console.log(res);

      localStorage.setItem('id', res.toString())
      //this.loaded=true;
      this.spinner.hide();
      this.route.navigate(['/audio'])

    },(err:any)=>{

    })


  }
}
