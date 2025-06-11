import { Injectable, NgZone } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SpeechRecognitionService {
  private recognition: any;

  constructor(private zone: NgZone) {
    const { webkitSpeechRecognition }: any = window as any;
    this.recognition = new webkitSpeechRecognition();
    this.recognition.continuous = true;  // Keep listening for continuous speech
    this.recognition.interimResults = true;  // Enable interim results (partial results)
    this.recognition.lang = 'en-US';
  }

  startListening(): Observable<string> {
    let lastTranscription = '';

    return new Observable(observer => {
      this.recognition.onresult = (event: any) => {
        // Handle final results only
        const transcript = event.results[event.results.length - 1][0].transcript;
        
        // Only emit when the result is final and different from the last one
        if (event.results[event.results.length - 1].isFinal && transcript !== lastTranscription) {
          lastTranscription = transcript;  // Update the last transcript
          this.zone.run(() => {
            observer.next(transcript); // Emit the final transcription
          });
        }
      };

      this.recognition.onerror = (event: any) => {
        this.zone.run(() => {
          observer.error(event.error); // Emit error if any
        });
      };

      this.recognition.onend = () => {
        this.zone.run(() => {
          observer.complete(); // Complete the observable if recognition ends
        });
      };

      this.recognition.start();  // Start listening
    });
  }

  stopListening() {
    this.recognition.stop();  // Stop speech recognition
  }

  speakText(text: string, lang: string = 'en-US') {
    console.log("1");

    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);
  
    const voices = synth.getVoices();
    const selectedVoice = voices.find(voice => voice.lang === lang);
    if (selectedVoice) {
      utterance.voice = selectedVoice;
    }
    console.log("2");
  
    synth.speak(utterance);
    console.log("3");

  }
  
  getRobotResponse(userInput: string): Observable<string> {
    
    // Here we mock the API response. Replace this with actual API call in a real-world scenario.
    const mockApiResponse:any = {
      "hello": "Hi there! How can I help you today?",
      "how are you": "I'm doing great, thanks for asking!",
      "bye": "Goodbye! Have a great day!"
    };

    return new Observable(observer => {
      const response = mockApiResponse[userInput.toLowerCase()] || "Sorry, I didn’t understand that.";
      observer.next(response);
      observer.complete();
    });
  }
}
