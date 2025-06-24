import requests
import time
from fastapi import HTTPException, Request, UploadFile,File,BackgroundTasks
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
    
    def build_prompt(self, history):
        prompt = "[INST] You are a helpful assistant.\n"
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            prompt += f"{role}: {msg['content']}\n"
        prompt += "Assistant:"
        return prompt

    async def getOutputFromHF(self, email, uniqueId):
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

    # This is your POST API to start conversation

    async def startConversation(self, backgroundTasks: BackgroundTasks,  request: Request):
        # print("Received request for ID:", id)

        # Step 1: Extract user input from request body
        body = await request.json()
        userResponse = body.get("userResponse", "").strip()
        print("User said:", userResponse)

        # Step 2: Handle empty input
        if not userResponse:
            return JSONResponse(
                content={"AiResponse": "Can you please repeat your answer? I was unable to hear you.", "next": False}
            )

        # Step 3: Get existing conversation from MongoDB
        # document = collection.find_one({"_id": ObjectId(id)})
        # if not document:
        #     return JSONResponse(
        #         content={"AiResponse": "Conversation not found.", "next": False},
        #         status_code=404
        #     )

        # Step 4: Create conversation history string
        history = await ConversationService().createConversationString(document, isHr=True)
        print("Conversation History:\n", history)

        # Step 5: Prepare AI prompt
        template = """You are a professional, knowledgeable, and friendly chatbot with 10 years of experience as an HR specialist. You are designed to conduct HR interviews for software developer positions. Your primary goal is to evaluate the candidate's professional background, assess their skills, and determine how well they fit with our company culture.

    Start the interview with an introduction, then proceed by asking relevant HR questions based on the candidate's responses. Keep the conversation focused, engaging, and structured.

    Current conversation:
    {history}
    Human: {input}
    AI Assistant:"""

        prompt = PromptTemplate(input_variables=["history", "input"], template=template)
        formattedPrompt = prompt.format(history=history, input=userResponse)
        print("Prompt sent to AI:\n", formattedPrompt)

        # Step 6: Get response from Mistral AI
        try:
            chain = llm | StrOutputParser()
            AiResponse = chain.invoke(formattedPrompt)
        except Exception as e:
            print("AI error:", str(e))
            return JSONResponse(
                content={"AiResponse": "Sorry, something went wrong while processing your response.", "next": False},
                status_code=500
            )

        print("AI Responded:", AiResponse)

        # Step 7: Save update in background (user + AI response)
        backgroundTasks.add_task(
            ConversationService().createUpdateConversation,
            id,
            userResponse,
            AiResponse
        )

        # Step 8: Return response to frontend
        return JSONResponse(content={"AiResponse": AiResponse, "next": True})



 