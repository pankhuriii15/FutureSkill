from typing import List, Optional
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: str = Field(..., description="user or assistant or system")
    content: str = Field(..., description="Chat message text")
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    site_context: Optional[str] = Field("Site: Metro Tower C, Mumbai. Current Phase: Superstructure RCC slab casting.", description="Active project context")
    api_key: Optional[str] = Field(None, description="Optional Gemini API key from client session")

class ChatResponse(BaseModel):
    reply: str
    references: List[str] = Field(default_factory=list)
    suggested_followups: List[str] = Field(default_factory=list)
    execution_mode: str = "demo_fallback"
