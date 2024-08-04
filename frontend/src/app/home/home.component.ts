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
    
    if (this.reactiveForm.invalid) {
      //alert('kkk')
      this.toastr.error('valid email id is required')
      return
    }
    else{
      this.spinner.show();
    }

    let payload = {
      email: this.reactiveForm.value.email,
      uniqueId: Date.now()
    }
    //console.log(this.obj);
    //this.service.createConvo()
    this.service.createConvo(payload).subscribe((res) => {

      console.log(res);
      //const obj=res;
      const result = (res as { result: { accessKey: string,id:string,secretKey:string } }).result;
      //const accessKey = obj.result.accessKey;
      localStorage.setItem('id',result.id);
      localStorage.setItem('accessKey', result.accessKey)
      localStorage.setItem('secretKey', result.secretKey)
      //console.log('---->',result.id,result.accessKey,result.secretKey)
      //this.loaded=true;
      this.spinner.hide();
      this.route.navigate(['/audio'])

    },(err:any)=>{

    })


  }
}
