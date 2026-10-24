from fastapi import APIRouter, HTTPException, status
from ..schemas.chat_schemas import ChatRequest, ChatResponse
from ..services.site_chatbot import answer_site_chat

router = APIRouter(prefix="/api", tags=["Construction Engineering Assistant"])

@router.post(
    "/site-chat",
    response_model=ChatResponse,
    summary="Multi-turn construction engineering assistant for IS codes, OSHA, and site Q&A"
)
async def site_chat_endpoint(request: ChatRequest):
    """
    Answers construction engineering and project management questions with IS 456, OSHA, and NBC 2016 citations.
    """
    if not request.messages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chat history must contain at least one message."
        )

    try:
        response = await answer_site_chat(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}"
        )
