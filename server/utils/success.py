from fastapi import status
from fastapi.responses import JSONResponse

def success(message:str ):
   response_content = {"message": message}  
   return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

def result(data:object ):
   response_content = {"result": data}  
   return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

def response(data:str ):
   return JSONResponse(content=data, status_code=status.HTTP_200_OK)
