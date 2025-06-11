from fastapi import APIRouter,UploadFile,File,BackgroundTasks
from services.hf_service import HFService

router = APIRouter()

hfService = HFService()

 
@router.post("/{id}")
async def startConversation(backgroundTasks: BackgroundTasks,id:str):
    return await hfService.startConversation(backgroundTasks,id)
 





