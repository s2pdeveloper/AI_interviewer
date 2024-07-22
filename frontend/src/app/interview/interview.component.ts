import { ChangeDetectorRef, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { AudioRecordingService } from '../audio-recording.service';
import { ConversationService } from '../services/conversation.service';
import { Subscription } from 'rxjs';
import { DomSanitizer } from '@angular/platform-browser';
import { NgxSpinnerService } from 'ngx-spinner';


@Component({
  selector: 'app-interview',
  templateUrl: './interview.component.html',
  styleUrls: ['./interview.component.css']

})
export class InterviewComponent implements OnInit {
  isRecording = false;
  audioURL: any;
  flag: boolean = false
  uploadFlag: boolean = false
  @ViewChild('audioPlayer') audioPlayer!: ElementRef<HTMLAudioElement>;
  audioSubscription: Subscription | null = null;
  audioURLServer: string | ArrayBuffer | null = null;
  constructor(private sanitizer: DomSanitizer, private audioRecordingService: AudioRecordingService, private cd: ChangeDetectorRef, private service: ConversationService, private spinner: NgxSpinnerService) { }
  id: any;
  data: any;
  isComputerAudio:boolean=true;
  isLoading:boolean=false;
  ngOnInit() {
    this.id = localStorage.getItem("id")
    let audio = new Audio();
    audio.src = "../../assets/response.mp3";

    audio.load();
    audio.play();
    audio.onended = () => {
      this.flag = true;
      console.log('ended')
      this.isComputerAudio=false;
      this.startRecording()
    }

    this.audioRecordingService.audioBlob$.subscribe(blob => {
      this.audioURL = window.URL.createObjectURL(blob);
     //this.onClick();

      //this.audioURL=blob;
      // this.audioPlayer.nativeElement.src = this.audioURL;
      //this.audioPlayer.nativeElement.src=window.URL.createObjectURL(blob);
      this.cd.detectChanges();
    });
  }

  startRecording() {
    this.isRecording = true;
    this.audioRecordingService.startRecording();
    this.uploadFlag = true;
    //this.stopRecording();
    //const micContainer = document.getElementsByClassName('mic-container')[0];
//micContainer.click();
// micContainer.addEventListener('click', (e)=> {
//   let elem = e.target;
  
//   elem?.classList.toggle('active');

    
  }

  async stopRecording() {
    this.isRecording = false;
    await this.audioRecordingService.stopRecording();
    this.uploadFlag = true;
    this.isLoading=true;
    //this.isComputerAudio=true;
    // this.onClick();
   
  }
  
  async onClick() {
    if (this.audioURL) {
      this.isLoading=true;
      // let ele=document.getElementById("circle");
      // ele?.classList.add("noAudio");
      this.spinner.show();

      // Fetch the blob data from the audioURL
      const response = await fetch(this.audioURL);
      const blob = await response.blob();

      // Create FormData and append the blob
      const formData = new FormData();
      formData.append('file', blob, 'recorded_audio.wav');

      // Call the service to upload
      this.service.startCono(this.id, formData).subscribe((buf: any) => {
        try {
          this.playAudioElement(buf)
          // let uintArray = new Uint8Array(buf)
          // let blob = new Blob([uintArray])
          // var url = window.URL.createObjectURL(blob)
          // let audio = new Audio();
          // audio.src = url;
          // audio.play();
        } catch (error) {
          console.log("error", error);

        }
       
      });
    } else {
      console.error('No audio recorded or audio URL is invalid.');
    }
  }

  

  playAudioElement(buf:any) {
    let uintArray = new Uint8Array(buf)
    let blob = new Blob([uintArray])
    var url = window.URL.createObjectURL(blob)
    let audio = new Audio();
    audio.src = url;
    
    this.spinner.hide();
    // let ele=document.getElementById("circle");
    //   ele?.classList.remove("noAudio");
    this.isLoading=false;
    this.isComputerAudio=true
    audio.play();
    audio.onended = () => {
      this.flag = true;
      console.log('ended')
      this.isComputerAudio=false;
      this.startRecording()
    }

  }


}


