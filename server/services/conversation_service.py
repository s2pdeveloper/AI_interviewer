import os
import openai
from gtts import gTTS
from bson import ObjectId
from config.mongo import mongo_client
from pymongo import ReturnDocument
from models.schemas import ConversationDO,MappingDO
from utils.background_exception import handleExceptions
db = mongo_client.get_database()
from fastapi import HTTPException, UploadFile,File,BackgroundTasks
from utils.success import success, result,response
from fastapi.responses import FileResponse, JSONResponse
import assemblyai as aai
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
collection = db["conversation"]

aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')
os.environ["LANGCHAIN_PROJECT"] = "S2PEDUTECH"
openai.api_key = os.getenv('OPENAI_API_KEY')
llm = OpenAI()

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
        
    async def deleteConversation(self,id):
        if id is None or not id:
            raise HTTPException(status_code=400, detail="Please Provide ID")
        collection.delete_one({"_id":ObjectId(id)})
        os.remove(f"files/{id}.mp3")
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
        for entry in document['mapping']:
            ai_part = f"AI Assistant: {entry['ai']}\n"
            human_part = f"Human: {entry['human']}\n"
            conversation_string += ai_part
            if  entry['human'] is not None:
                conversation_string += human_part
                
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
        update_data = MappingDO(human=userResponse,ai= document["mapping"][last_index]['ai'])
        new_data = MappingDO(ai=aiResponse)
        print("update_data-----",update_data)
        # update_data = {f"mapping.{last_index}.human": userResponse}
        print("new_data-----",new_data)
        
        # updated_document = collection.find_one_and_update(
        #     update_query,
        #     {"$set": {"mapping.-1": update_data.dict()}},
        #     return_document=ReturnDocument.AFTER
        # )
        updated_document = collection.find_one_and_update(
        update_query,
        {"$set": {"mapping.$[lastElem]": update_data.dict()}},
        array_filters=[{"lastElem": {"$exists": True}}],
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
    
    async def startConversation(self,backgroundTasks:BackgroundTasks,id:str,file: UploadFile = File(...)):
        print("id----file----",id,file)
        # return await self.createUpdateConversation(id,"My name is Pooja. I am a software developer. I work in Node Js and Java and in front end I work on angular and ionic.","That's great, Pooja. Why did you choose to become a software developer?")
        file_location = f"files/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        userResponse = await self.transcribeSpeech(file_location)
        print("userResponse-------",userResponse)
        if not userResponse or userResponse is None:
            interruptPrompt = "Can you please repeat your answer? I was unable to hear you."
            tts = gTTS(text=AiResponse, lang='en', tld='co.uk')
            filePath = f"files/{id}.mp3"
            print("filePath-----",filePath)
            tts.save(filePath)
            return FileResponse(path=filePath, media_type='audio/mpeg', filename=f"{id}.mp3")
            
            
        if userResponse or userResponse is not None:
            os.remove(file_location)
            
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
        AiResponse = llm.invoke(formattedPrompt)
        print("AiResponse-----",AiResponse)
        tts = gTTS(text=AiResponse, lang='en', tld='co.uk')
        filePath = f"files/{id}.mp3"
        print("filePath-----",filePath)
        tts.save(filePath)
        backgroundTasks.add_task(self.createUpdateConversation,id,userResponse,AiResponse)
        return FileResponse(path=filePath, media_type='audio/mpeg', filename=f"{id}.mp3")
    
    async def uploadConversation(self,file: UploadFile = File(...)):
        os.makedirs("files", exist_ok=True)
        file_location = f"files/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        return JSONResponse(content={"filename": file.filename})  