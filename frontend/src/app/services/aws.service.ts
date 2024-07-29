import { Injectable } from '@angular/core';
import * as AWS from 'aws-sdk'
import * as S3 from 'aws-sdk/clients/s3';

@Injectable({
  providedIn: 'root'
})
export class AwsService {

    bucket = new S3({
    
    region: 'ap-south-1'
  });
  

  constructor() { }
  async uploadFile(key:string,file:any) {

    console.log('file----',file)
   
    const contentType = file.type;
 

      const params={
        Bucket:'s2p-ai-interview',
        Key:`${key}/input`,
        Body:file,
        ContentType: contentType
      };
      let  result = await this.bucket.upload(params).promise()
    
    return result;
  }
}
