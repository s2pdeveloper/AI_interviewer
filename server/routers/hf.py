from fastapi import APIRouter, Request,UploadFile,File,BackgroundTasks
from services.hf_service import HFService

router = APIRouter()

hfService = HFService()

 
@router.post("/")
async def startConversation(backgroundTasks: BackgroundTasks,request:Request):
    return await hfService.startConversation(backgroundTasks,request)
 





