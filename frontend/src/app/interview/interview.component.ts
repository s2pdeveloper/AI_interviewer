import { ChangeDetectorRef, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { AudioRecordingService } from '../audio-recording.service';
import { ConversationService } from '../services/conversation.service';
import { Subscription } from 'rxjs';
import { DomSanitizer } from '@angular/platform-browser';
import { NgxSpinnerService } from 'ngx-spinner';
import { AwsService } from '../services/aws.service';
import { Router, ActivatedRoute } from '@angular/router';



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
  @ViewChild('msg', { static: true }) msgElement!: ElementRef;
  audioSubscription: Subscription | null = null;
  audioURLServer: string | ArrayBuffer | null = null;

  constructor(private sanitizer: DomSanitizer, private audioRecordingService: AudioRecordingService, private cd: ChangeDetectorRef, private service: ConversationService, private spinner: NgxSpinnerService, private awsService: AwsService, private route: Router
  ) { }
  id: any;
  data: any;
  isComputerAudio: boolean = true;
  isLoading: boolean = false;
  ngOnInit() {

    this.id = localStorage.getItem("id")
    let audio = new Audio();
    audio.src = "../../assets/response.mp3";

    audio.load();
    audio.play();
    this.showText("AI: Hello, I will be conducting your interview today. Let's start with the first question: Can you tell me about yourself?", 0, 80);
    audio.onended = () => {
      this.flag = true;
      console.log('ended')
      this.isComputerAudio = false;
      this.startRecording()
    }

    this.audioRecordingService.audioBlob$.subscribe(blob => {
      this.audioURL = window.URL.createObjectURL(blob);
      this.isComputerAudio = true;
      this.onClick();

      //this.audioURL=blob;
      // this.audioPlayer.nativeElement.src = this.audioURL;
      //this.audioPlayer.nativeElement.src=window.URL.createObjectURL(blob);
      this.cd.detectChanges();
    });
  }

  startRecording() {
    this.isRecording = true;
    this.audioRecordingService.startRecording();
    //this.uploadFlag = true;

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
    this.isLoading = true;
    //this.isComputerAudio=true;
    // this.onClick();

  }

  async onClick() {
    if (this.audioURL) {
      this.isLoading = true;
      // let ele=document.getElementById("circle");
      // ele?.classList.add("noAudio");
      this.spinner.show();

      // Fetch the blob data from the audioURL
      const response = await fetch(this.audioURL);
      const blob = await response.blob();

      // Create FormData and append the blob
      const formData = new FormData();
      formData.append('file', blob, 'recorded_audio.wav');
      let data = await this.awsService.uploadFile(this.id, blob)
      console.log('data------', data.Key);
      // return
      // Call the service to upload
      this.service.startCono(this.id).subscribe((buf: any) => {
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



  playAudioElement(buf: any) {
    let uintArray = new Uint8Array(buf)
    let blob = new Blob([uintArray])
    var url = window.URL.createObjectURL(blob)
    let audio = new Audio();
    audio.src = url;

    this.spinner.hide();
    // let ele=document.getElementById("circle");
    //   ele?.classList.remove("noAudio");
    this.isLoading = false;
    this.isComputerAudio = true
    audio.play();
    this.msgElement.nativeElement.textContent = '';
    this.showText("AI: hey this next sample question", 0, 80);
    audio.onended = () => {
      this.flag = true;
      console.log('ended')
      this.isComputerAudio = false;
      this.startRecording()
    }

  }
  viewResult() {
    this.route.navigateByUrl('/result');
  }
  showText(message: string, index: number, interval: number) {

    if (index < message.length) {
      this.msgElement.nativeElement.textContent += message[index++];
      setTimeout(() => this.showText(message, index, interval), interval);
    }

  }


}


