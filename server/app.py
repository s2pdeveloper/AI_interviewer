from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import conversation
from utils.global_exception import CustomExceptionHandler
app = FastAPI(swagger_ui_parameters={"displayRequestDuration": True})
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CustomExceptionHandler)
@app.get("/healthCheck")
async def read_root():
    return {"message": "Server is Running"}


app.include_router(conversation.router,
    prefix="/conversation",
    tags=["Conversation"])



