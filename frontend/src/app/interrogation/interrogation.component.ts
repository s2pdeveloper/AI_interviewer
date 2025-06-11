import { AfterViewInit, Component, NgZone, OnInit } from '@angular/core';
import { SpeechRecognitionService } from '../services/speech.service';
import { log } from 'console';
declare var webkitSpeechRecognition: any;
@Component({
  selector: 'app-interrogation',
  templateUrl: './interrogation.component.html',
  styleUrls: ['./interrogation.component.css']
})
export class InterrogationComponent implements OnInit {
  // spokenText: string = ''
  // textToSpeech: string = 'Hi this is new bot created by S2P'
  // isLoading: boolean = false;
  recognition: any;
  finalTranscript = '';
  interimTranscript = '';
  pauseTimer: any;
  userText = '';
  botResponse = '';
  isListening = false;
  synth = window.speechSynthesis;
  voices: SpeechSynthesisVoice[] = [];
  isSpeaking = false;

  constructor(private speech: SpeechRecognitionService, private zone: NgZone) { }
  // ngAfterViewInit(): void {
  //   this.simulateUserInteraction();
  //   this.speech.startListening().subscribe({
  //     next: (text: any) => {
  //       this.spokenText = text
  //       this.getRobotResponse(this.spokenText);
  //     },
  //     error: (e: any) => { console.log(e) }
  //   })
  // }


  // simulateUserInteraction() {
  //   console.log('click 1');

  //   const button = document.getElementById('speakBtn') as HTMLButtonElement;  // Get the button by id

  //   if (button) {
  //     console.log('click 1', button);

  //     button.click();  // Trigger the button click programmatically
  //   }


  // }


  ngOnInit(): void {
    this.initSpeechRecognition();
    // this.startConversation();

    // console.log('Speech synthesis supported:', 'speechSynthesis' in window);
    // console.log('Speech recognition supported:', 'webkitSpeechRecognition' in window);
    this.loadVoices();
    // In case voices load after ngOnInit (which happens sometimes)
    window.speechSynthesis.onvoiceschanged = () => this.loadVoices();

  }

  // speak(text: any = this.textToSpeech) {
  //   this.speech.speakText(text)
  // }

  // stopListening() {
  //   this.speech.stopListening()
  //   console.log(this.spokenText)
  // }


  // getRobotResponse(input: string) {
  //   // Call the API to get the robot's response
  //   this.speech.getRobotResponse(input)
  //     .subscribe(response => {
  //       this.textToSpeech = response;
  //       this.speak(response);  // Make the robot speak the response
  //       console.log('response', response);

  //     }, error => {
  //       console.error('Error fetching response:', error);
  //       this.textToSpeech = 'Sorry, there was an error processing your request.';
  //       this.speak(this.textToSpeech);  // Error fallback message
  //     });
  // }


  startConversation() {
    this.speak('How can I help you?', () => {
      this.startListening();
    });
  }

  initSpeechRecognition() {
    this.recognition = new webkitSpeechRecognition();
    this.recognition.continuous = true; // Important for long speech
    this.recognition.interimResults = true;
    this.recognition.lang = 'en-US';

    this.recognition.onresult = (event: any) => {


      this.interimTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          this.finalTranscript += transcript + ' ';
        } else {
          this.interimTranscript += transcript;
        }
      }

      // console.log('Interim:', this.interimTranscript);
      // console.log('Final:', this.finalTranscript);

      this.resetPauseTimer();
    };

    this.recognition.onend = () => {
      console.log('Recognition ended');
    };

    this.recognition.onerror = (event: any) => {
      console.error('Recognition error:', event.error);
    };
  }

  startListening() {
    this.finalTranscript = '';
    this.interimTranscript = '';
    this.userText = '';
    this.isListening = true;
    this.recognition.start();
  }

  resetPauseTimer() {
    if (this.pauseTimer) {
      clearTimeout(this.pauseTimer);
    }

    this.pauseTimer = setTimeout(() => {
      this.stopListeningAndSend();
    }, 2500); // 2 seconds pause threshold
  }

  stopListeningAndSend() {
    this.isListening = false;
    this.recognition.stop();
    const message = this.finalTranscript.trim();
    this.userText = message;
    if (message) {
      this.sendToServer(message);
    } else {
      this.speak("I didn't catch that. Can you say it again?", () => {
        this.startListening();
      });
    }
  }

  speak(text: string, onComplete?: () => void) {
    const utterance = new SpeechSynthesisUtterance(text);
    // console.log('utterance:', utterance);

    //    // Optional: set voice by language or name
    // const selectedVoice = this.voices.find(v => v.lang === 'en-US' && v.name.includes('Google'));
    // if (selectedVoice) {
    //   utterance.voice = selectedVoice;
    // }

    // utterance.lang = 'hi-IN'; // Optional if voice is already set
    // utterance.rate = 1;       // Speed: 0.1 - 10
    // utterance.pitch = 1; 

    utterance.onstart = () => {
      this.zone.run(() => {

        this.isSpeaking = true; // Start animation
        console.log('this.isSpeaking', this.isSpeaking);
      })

    };

    utterance.onend = () => {
      this.zone.run(() => {

        this.isSpeaking = false;
        console.log('this.isSpeaking', this.isSpeaking);

        if (onComplete) onComplete();
      })

    };
    this.synth.speak(utterance);
    // window.speechSynthesis.speak(utterance);
    console.log('Speaking:', text);

  }
  sendToServer(text: string) {
    const payload = { message: text };

    // this.http.post<{ response: string }>('https://your-api.com/bot-reply', payload)
    //   .subscribe(
    //     (res) => {
    const botResponse = "aur kya kar rha h bhai";
    this.speak(botResponse, () => {
      this.startListening(); // 🔁 start again after bot finishes speaking
    });
    //   },
    //   (err) => {
    //     console.error('API Error:', err);
    //     this.speak("Sorry, something went wrong.", () => {
    //       this.startListening();
    //     });
    //   }
    // );
  }

  loadVoices() {
    this.voices = window.speechSynthesis.getVoices();
    // console.log('Available voices:', this.voices);
  }

}
