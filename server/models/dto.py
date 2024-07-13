from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from fastapi import UploadFile,File


class ConversationData(BaseModel):
    id:str
    file: UploadFile = File(...)