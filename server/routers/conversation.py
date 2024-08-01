from fastapi import APIRouter,UploadFile,File,BackgroundTasks
from services.conversation_service import ConversationService

router = APIRouter()

conversationService = ConversationService()

@router.post("")
async def createConversation(email:str,uniqueId:str):
    return await conversationService.createConversation(email,uniqueId)

@router.delete("/{id}")
async def deleteConversation(id:str):
    return await conversationService.deleteConversation(id)

@router.put("/{id}")
async def startConversation(backgroundTasks: BackgroundTasks,id:str):
    return await conversationService.startConversation(backgroundTasks,id)

@router.post("/upload")
async def uploadConversation(file: UploadFile = File(...)):
    return await conversationService.uploadConversation(file)

@router.get("/{id}")
async def result(backgroundTasks: BackgroundTasks,id:str):
    return await conversationService.result(backgroundTasks,id)





