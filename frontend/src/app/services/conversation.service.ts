import { Injectable } from '@angular/core';
import { catchError, map, Observable, Subject } from 'rxjs'; 
import {HttpClient, HttpParams, HttpResponse} from '@angular/common/http'
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ConversationService {

    routes={
        startConversationPath:(id:any)=>`${environment.baseUrl}/conversation/${id}`,
        getConversationPath:(id:any)=>`${environment.baseUrl}/conversation/${id}`,
        createConversationPath:(payload:any)=>`${environment.baseUrl}/conversation?email=${payload.email}&uniqueId=${payload.uniqueId}`,
    }

  
  constructor(private http:HttpClient){

  }

  createConvo(pyload:any){
    return this.http.post(this.routes.createConversationPath(pyload),null)
  }
 
  startCono(id:any){
    return this.http.put(this.routes.startConversationPath(id),'',{responseType:'arraybuffer'}
      )
  }
  getConvo(id:any){
    return this.http.get(this.routes.getConversationPath(id));
  }

  getAudioFile(id: any): Observable<string | ArrayBuffer | null> {
    const url = `${environment.baseUrl}/${id}`; // Adjust URL based on your backend API

    // Handle the response as text (since it's mistakenly set as application/json)
    return this.http.get(url, {
      responseType: 'text',
      observe: 'response'
    }).pipe(
      catchError(error => {
        console.error('Error fetching audio file:', error);
        throw error; // Handle or rethrow error as needed
      }),
      map(response => {
        // Assuming the server sends the audio file content in response body
        const audioContent:any = response.body;

        // Create a blob from the response data
        const blob = new Blob([audioContent], { type: 'audio/wav' });

        // Create a URL for the Blob object received
        return window.URL.createObjectURL(blob);
      })
    );
  }
  
}
