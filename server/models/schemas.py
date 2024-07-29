from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class MappingDO(BaseModel):
    human:Optional[str] = Field(default=None)  
    ai:Optional[str] = Field(default=None)  

        
class ConversationDO(BaseModel):
     email: str
     uniqueId:str
     mapping:Optional[List[MappingDO]] = Field(default=None)  

    