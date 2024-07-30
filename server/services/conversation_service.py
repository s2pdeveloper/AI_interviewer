import json
import os
import openai
from gtts import gTTS
from bson import ObjectId
from config.mongo import mongo_client
from pymongo import ReturnDocument
from models.schemas import ConversationDO,MappingDO
from config.credentials import ServiceConstant
from utils.background_exception import handleExceptions
db = mongo_client.get_database()
from fastapi import HTTPException, UploadFile,File,BackgroundTasks
from utils.success import success, result,response
from fastapi.responses import FileResponse, JSONResponse, Response
import assemblyai as aai
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain.schema import SystemMessage, HumanMessage
import boto3
from langchain.schema import StrOutputParser

session = boto3.Session(
    aws_access_key_id=ServiceConstant.access_key,
    aws_secret_access_key=ServiceConstant.secret_access_key,
    region_name=ServiceConstant.region
)

collection = db["conversation"]

aai.settings.api_key = ServiceConstant.assemblyai_api_key
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = ServiceConstant.langchain_api_key
os.environ["LANGCHAIN_PROJECT"] = ServiceConstant.project_name
openai.api_key = ServiceConstant.openai_api_key
# llm = OpenAI()
llm = ChatOpenAI(model_name=ServiceConstant.model, temperature=ServiceConstant.temperature)

class ConversationService:
    def __init__(self):
        pass
    
    async def createConversation(self,email,uniqueId):
        if email is None or not email:
            raise HTTPException(status_code=400, detail="Please Provide Email")
        
        mappingDO = MappingDO(ai="Hello, I will be conducting your interview today. Let's start with the first question: Can you tell me about yourself?")
        conversationDO = ConversationDO(email=email,uniqueId=uniqueId,mapping=[mappingDO])
        responseData = collection.update_one(
                {"uniqueId": uniqueId},  # Filter criteria
                {"$setOnInsert": conversationDO.dict()},  # Update document with $setOnInsert
                upsert=True
                )
        print("responseData---",responseData)
        if responseData.upserted_id is not None:
            return response(str(responseData.upserted_id))
        else:
            return response(None)
    
    async def result(self,backgroundTasks: BackgroundTasks,id:str):
        document = collection.find_one({"_id":ObjectId(id)})
        conversation = await self.createConversationString(document)
        print("conversation----",conversation)
        output ="""[
                {
                    "Question":"",
                    "Human Answer":""
                    "Improved Answer":""
                    "Rating":""
                }
                ]"""
        template ="""This is the Interview conversation:
        {conversation}
        output:
        {outputJson}
        You need to observe the conversation and providing rating out of 5 to  Human each answer  and provide improved answer to Each question in the following json format"""
        prompt = PromptTemplate(input_variables=["conversation", "outputJson"], template=template)
        formattedPrompt = prompt.format(conversation=conversation, outputJson=output)
        print("prompt-----",formattedPrompt)
        system_prompt = "You are an AI assistant who is expert in taking interview"
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=formattedPrompt)
            ]
        chain = llm | JsonOutputParser()
        response = chain.invoke(messages)
        print(response)
        # backgroundTasks.add_task(self.deleteConversation,id)
        return response
            
    async def deleteConversation(self,id):
        if id is None or not id:
            raise HTTPException(status_code=400, detail="Please Provide ID")
        collection.delete_one({"_id":ObjectId(id)})
        os.remove(f"files/{id}.mp3")
        self.deleteFolder(id)
        return success("Conversation Deleted Successfully!")
        
    async def transcribeSpeech(self,file_path):
        transcriber = aai.Transcriber()

        transcript = transcriber.transcribe(file_path)
        if transcript.error:
            print(transcript.error)
        else:
            print(transcript.text)
            return transcript.text   
        
    async def createConversationString(self,document):
        conversation_string = ""
        print("document['mapping']---",document['mapping'])
        for entry in document['mapping']:
            print(entry)
            ai_part = f"AI Assistant: {entry['ai']}\n"
            human_part = f"Human: {entry['human']}\n"
            conversation_string += ai_part
            print( entry['human'] is not None)
            if  entry['human'] is not None:
                conversation_string += human_part
            print("conversation_string----",conversation_string)
                
        return conversation_string
    
    @handleExceptions
    async def createUpdateConversation(self,id,userResponse,aiResponse):
        document = collection.find_one({"_id": ObjectId(id)})
        if document is None or "mapping" not in document or not document["mapping"]:
            raise HTTPException(status_code=404, detail="Document or mapping array not found")

        # Update the 'human' key in the last object of the 'mapping' array
        last_index = len(document["mapping"]) - 1
        print("document-----",document)
        print("last_index-----",last_index)
        print("document['ai']---",document["mapping"][last_index]['ai'])
        update_query = {"_id": ObjectId(id)}
        # update_data = MappingDO(human=userResponse,ai= document["mapping"][last_index]['ai'])
        new_data = MappingDO(ai=aiResponse)
        # print("update_data-----",update_data)
        # update_data = {f"mapping.{last_index}.human": userResponse}
        print("new_data-----",new_data)
        
        # updated_document = collection.find_one_and_update(
        #     update_query,
        #     {"$set": {"mapping.-1": update_data.dict()}},
        #     return_document=ReturnDocument.AFTER
        # )
        # updated_document = collection.find_one_and_update(
        # update_query,
        # {"$set": {"mapping.$[lastElem]": update_data.dict()}},
        # array_filters=[{"lastElem": {"$exists": True}}],
        # return_document=ReturnDocument.AFTER
        # )
        updated_document = collection.find_one_and_update(
            update_query,
            {"$set": {f"mapping.{last_index}.human": userResponse}},
            return_document=ReturnDocument.AFTER
        )
        print("updated_document-----first",updated_document)
        
        if updated_document is None:
            raise HTTPException(status_code=404, detail="Document not found")

        # Add the new object to the array
        updated_document = collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$push": {"mapping": new_data.dict()}},
            return_document=ReturnDocument.AFTER
        )
        
        print("updated_document-----final",updated_document)
        
        if updated_document is None:
            raise HTTPException(status_code=404, detail="Document not found")

        return updated_document
    
    async def startConversation(self,backgroundTasks:BackgroundTasks,id:str):
        print("id----file----",id)
        # return await self.createUpdateConversation(id,"My name is Pooja. I am a software developer. I work in Node Js and Java and in front end I work on angular and ionic.","That's great, Pooja. Why did you choose to become a software developer?")
        # file_location = f"files/{file.filename}"
        # with open(file_location, "wb+") as file_object:
        #     file_object.write(file.file.read())

        userResponse = await self.transcribeSpeech(f"{ServiceConstant.s3_bucket_url}{id}/input")
        print("userResponse-------",userResponse)
        if not userResponse or userResponse is None:
            AiResponse = "Can you please repeat your answer? I was unable to hear you."
            tts = gTTS(text=AiResponse, lang='en', tld='co.uk')
            filePath = f"files/{id}.mp3"
            print("filePath-----",filePath)
            tts.save(filePath)
            
            backgroundTasks.add_task(self.deleteFromS3,f"{id}/input")
            
            with open(filePath, "rb") as audio_file:
                audio_content = audio_file.read()

            # Create the multipart response
            boundary = "custom-boundary"
            multipart_response = (
                f"--{boundary}\r\n"
                f"Content-Disposition: form-data; name=\"response\"\r\n"
                f"Content-Type: application/json\r\n\r\n"
                f"{json.dumps({'AiResponse': AiResponse,'next':False})}\r\n"
                f"--{boundary}\r\n"
                f"Content-Disposition: form-data; name=\"audio\"; filename=\"{id}.mp3\"\r\n"
                f"Content-Type: audio/mpeg\r\n\r\n"
            ).encode() + audio_content + f"\r\n--{boundary}--\r\n".encode()

            return Response(
                content=multipart_response,
                media_type=f"multipart/form-data; boundary={boundary}"
            )
            # return FileResponse(path=filePath, media_type='audio/mpeg', filename=f"{id}.mp3")
            
            
        # if userResponse or userResponse is not None:
        #     os.remove(file_location)
            
        document = collection.find_one({"_id":ObjectId(id)})
        
        history = await self.createConversationString(document)
       
        print("history-----",history)
        template = """You are a professional, knowledgeable, and friendly chatbot with 10 years of experience as an HR specialist. You are designed to conduct HR interviews for software developer positions. Your primary goal is to evaluate the candidate's professional background, assess their skills, and determine how well they fit with our company culture. 

            Start the interview with an introduction, then proceed by asking relevant HR questions based on the candidate's responses. Keep the conversation focused, engaging, and structured. Here are some types of questions you might ask, but feel free to adapt based on the candidate's answers:

            - Can you tell me about yourself and your professional background?
            - Why did you choose to become a software developer?
            - What programming languages are you most comfortable with?
            - Can you describe a challenging project you worked on and how you overcame the challenges?
            - How do you stay updated with the latest developments in software development?
            - Can you give an example of a time when you had to work as part of a team? What was your role, and how did you contribute to the team's success?
            - How do you handle tight deadlines and pressure at work?
            - What do you know about our company, and why do you want to work here?
            - Can you describe a situation where you had to learn a new technology or tool quickly? How did you approach it?
            - How do you prioritize your tasks and manage your time effectively?
            - What are your strengths and weaknesses as a software developer?

            Current conversation:
            {history}
            Human: {input}
            AI Assistant:"""
        prompt = PromptTemplate(input_variables=["history", "input"], template=template)
        formattedPrompt = prompt.format(history=history, input=userResponse)
        print("prompt-----",formattedPrompt)
        chain = llm | StrOutputParser()
        AiResponse = chain.invoke(formattedPrompt)
        print("AiResponse-----",AiResponse)
        tts = gTTS(text=AiResponse, lang='en', tld='co.uk')
        filePath = f"files/{id}.mp3"
        print("filePath-----",filePath)
        tts.save(filePath)
        backgroundTasks.add_task(self.deleteFromS3,f"{id}/input")
        backgroundTasks.add_task(self.createUpdateConversation,id,userResponse,AiResponse)
        # return FileResponse(path=filePath, media_type='audio/mpeg', filename=f"{id}.mp3")
          # Read the audio file content
        with open(filePath, "rb") as audio_file:
            audio_content = audio_file.read()

        # Create the multipart response
        boundary = "custom-boundary"
        multipart_response = (
            f"--{boundary}\r\n"
            f"Content-Disposition: form-data; name=\"response\"\r\n"
            f"Content-Type: application/json\r\n\r\n"
            f"{json.dumps({'AiResponse': AiResponse,'next':True})}\r\n"
            f"--{boundary}\r\n"
            f"Content-Disposition: form-data; name=\"audio\"; filename=\"{id}.mp3\"\r\n"
            f"Content-Type: audio/mpeg\r\n\r\n"
        ).encode() + audio_content + f"\r\n--{boundary}--\r\n".encode()

        return Response(
            content=multipart_response,
            media_type=f"multipart/form-data; boundary={boundary}"
        )
    
    @handleExceptions
    async def deleteFromS3(self,key):
        s3 = session.client('s3')
        s3.delete_object(Bucket=ServiceConstant.s3_bucket_name, Key=key)
    
    @handleExceptions
    async def deleteFolder(self,folderName):
        s3 = session.resource('s3')
        bucket = s3.Bucket(ServiceConstant.s3_bucket_name)
        bucket.objects.filter(Prefix=folderName).delete()
        
    async def uploadConversation(self,file: UploadFile = File(...)):
        os.makedirs("files", exist_ok=True)
        file_location = f"files/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        return JSONResponse(content={"filename": file.filename})  