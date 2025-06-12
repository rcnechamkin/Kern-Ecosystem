from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.llm.kern_chat import kern_chat
import logging

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI router instance
router = APIRouter()

# Define request model
class ChatRequest(BaseModel):
    intent: str
    user_input: str

# Define the route
@router.post("/llm/chat")
async def chat_endpoint(payload: ChatRequest):
    logger.info(f"/llm/chat called with: intent='{payload.intent}', user_input='{payload.user_input}'")

    try:
        response = kern_chat(intent=payload.intent, user_input=payload.user_input)
        logger.info(f"kernel_chat returned: {response}")
        return {"response": response.choices[0].message.content.strip()}
    except Exception as e:
        logger.error(f"kern_chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
