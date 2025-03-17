from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.llm_service import LLMService
from app.services.memory_service import MemoryService

app = FastAPI()
memory = MemoryService()
llm_service = LLMService(memory)
class ChatRequestModel(BaseModel):
    """Request model for chat API."""
    user_input: str
    model_name: str

@app.post("/chat", response_class=StreamingResponse)
async def chat_response(request: ChatRequestModel):
    """
    Chat endpoint that streams AI-generated responses.

    Args:
        request (ChatRequestModel): The request body containing user input and model selection.

    Returns:
        StreamingResponse: A streamed response from the AI model.
    """
    return StreamingResponse(
        llm_service.generate_response(request.user_input, request.model_name), 
        media_type="text/plain"
    )

@app.get("/", response_model=str)
async def health_check():
    """
    Health check endpoint to verify API status.

    Returns:
        str: A simple message indicating the API is running.
    """
    return "API is Running"


@app.get("/chat-history", response_model = dict)
async def chat_history():
    """
    Chat History Endpoint that returns the chat history. 

    Returns:  
        dict: A dictionary response of the entire chat history.
    """
    return memory.get_conversation_history()



