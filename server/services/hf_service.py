import requests
import time
from fastapi import HTTPException, UploadFile,File,BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse, Response

# Hugging Face token and endpoint 
hf_token = ""   
model_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

# Headers
headers = {
    "Authorization": f"Bearer {hf_token}",
    "Content-Type": "application/json"
}
 
chat_history = []

class HFService:
    def __init__(self):
        pass
    
    def build_prompt(history):
        prompt = "[INST] You are a helpful assistant.\n"
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            prompt += f"{role}: {msg['content']}\n"
        prompt += "Assistant:"
        return prompt

    
    async def getOutputFromHF(self,email,uniqueId):
            user_input = input("👤 You: ")
            # if user_input.lower() == "exit":
            #     print("👋 Ending chat.")
            #     break

            chat_history.append({"role": "user", "content": user_input})
            prompt = self.build_prompt(chat_history)

            # Time start
            start_time = time.time()

            response = requests.post(model_url, headers=headers, json={"inputs": prompt})

            # Time end
            end_time = time.time()
            response_time = end_time - start_time

            if response.status_code == 200:
                try:
                    output = response.json()
                    generated = ""
                    if isinstance(output, list) and "generated_text" in output[0]:
                        generated = output[0]["generated_text"]
                    elif "generated_text" in output:
                        generated = output["generated_text"]

                    assistant_reply = generated.split("Assistant:")[-1].strip()
                    print(f"🤖 Mistral: {assistant_reply}")
                    print(f"⏱️ Response Time: {response_time:.2f} seconds\n")

                    chat_history.append({"role": "assistant", "content": assistant_reply})

                except Exception as e:
                    print("⚠️ Error parsing response:", e)
                    print(response.text)
            else:
                print(f"❌ Failed (Status {response.status_code}): {response.text}")
                return
            
    async def startConversation(self,backgroundTasks:BackgroundTasks,id:str,userResponse):
        print("id----file----",id)
        # return await self.createUpdateConversation(id,"My name is Pooja. I am a software developer. I work in Node Js and Java and in front end I work on angular and ionic.","That's great, Pooja. Why did you choose to become a software developer?")
        # file_location = f"files/{file.filename}"
        # with open(file_location, "wb+") as file_object:
        #     file_object.write(file.file.read())

        # userResponse = await self.transcribeSpeech(f"{ServiceConstant.s3_bucket_url}{id}/input")
        # print("userResponse-------",userResponse)
        # if not userResponse or userResponse is None:
        #     AiResponse = "Can you please repeat your answer? I was unable to hear you."
        #     tts = gTTS(text=AiResponse, lang='en', tld='co.uk')
        #     filePath = f"files/{id}.mp3"
        #     print("filePath-----",filePath)
        #     tts.save(filePath)
            
        #     backgroundTasks.add_task(self.deleteFromS3,f"{id}/input")
            
        #     with open(filePath, "rb") as audio_file:
        #         audio_content = audio_file.read()

            # # Create the multipart response
            # boundary = "custom-boundary"
            # multipart_response = (
            #     f"--{boundary}\r\n"
            #     f"Content-Disposition: form-data; name=\"response\"\r\n"
            #     f"Content-Type: application/json\r\n\r\n"
            #     f"{json.dumps({'AiResponse': AiResponse,'next':False})}\r\n"
            #     f"--{boundary}\r\n"
            #     f"Content-Disposition: form-data; name=\"audio\"; filename=\"{id}.mp3\"\r\n"
            #     f"Content-Type: audio/mpeg\r\n\r\n"
            # ).encode() + audio_content + f"\r\n--{boundary}--\r\n".encode()

            # return Response(
            #     content=multipart_response,
            #     media_type=f"multipart/form-data; boundary={boundary}"
            # )
            # # return FileResponse(path=filePath, media_type='audio/mpeg', filename=f"{id}.mp3")
            
            
        # if userResponse or userResponse is not None:
        #     os.remove(file_location)
            
        # document = collection.find_one({"_id":ObjectId(id)})
        
        # history = await self.createConversationString(document,False)
       
        # print("history-----",history)
        # template = """You are a professional, knowledgeable, and friendly chatbot with 10 years of experience as an HR specialist. You are designed to conduct HR interviews for software developer positions. Your primary goal is to evaluate the candidate's professional background, assess their skills, and determine how well they fit with our company culture. 

        #     Start the interview with an introduction, then proceed by asking relevant HR questions based on the candidate's responses. Keep the conversation focused, engaging, and structured. Here are some types of questions you might ask, but feel free to adapt based on the candidate's answers:

            # - Can you tell me about yourself and your professional background?
            # - Why did you choose to become a software developer?
            # - What programming languages are you most comfortable with?
            # - Can you describe a challenging project you worked on and how you overcame the challenges?
            # - How do you stay updated with the latest developments in software development?
            # - Can you give an example of a time when you had to work as part of a team? What was your role, and how did you contribute to the team's success?
            # - How do you handle tight deadlines and pressure at work?
            # - What do you know about our company, and why do you want to work here?
            # - Can you describe a situation where you had to learn a new technology or tool quickly? How did you approach it?
            # - How do you prioritize your tasks and manage your time effectively?
            # - What are your strengths and weaknesses as a software developer?

            # Current conversation:
            # {history}
            # Human: {input}
            # AI Assistant:"""
        # prompt = PromptTemplate(input_variables=["history", "input"], template=template)
        # formattedPrompt = prompt.format(history=history, input=userResponse)
        # print("prompt-----",formattedPrompt)
        # chain = llm | StrOutputParser()
        # AiResponse = chain.invoke(formattedPrompt)
        # print("AiResponse-----",AiResponse)
        # tts = gTTS(text=AiResponse, lang='en', tld='co.uk')
        # filePath = f"files/{id}.mp3"
        # print("filePath-----",filePath)
        # tts.save(filePath)
        # backgroundTasks.add_task(self.deleteFromS3,f"{id}/input")
        # backgroundTasks.add_task(self.createUpdateConversation,id,userResponse,AiResponse)
        # # return FileResponse(path=filePath, media_type='audio/mpeg', filename=f"{id}.mp3")
        #   # Read the audio file content
        # with open(filePath, "rb") as audio_file:
        #     audio_content = audio_file.read()

        # # Create the multipart response
        # boundary = "custom-boundary"
        # multipart_response = (
        #     f"--{boundary}\r\n"
        #     f"Content-Disposition: form-data; name=\"response\"\r\n"
        #     f"Content-Type: application/json\r\n\r\n"
        #     f"{json.dumps({'AiResponse': AiResponse,'next':True})}\r\n"
        #     f"--{boundary}\r\n"
        #     f"Content-Disposition: form-data; name=\"audio\"; filename=\"{id}.mp3\"\r\n"
        #     f"Content-Type: audio/mpeg\r\n\r\n"
        # ).encode() + audio_content + f"\r\n--{boundary}--\r\n".encode()
        
        res = self.getOutputFromHF()

        return Response(
            content=res, 
        )


 