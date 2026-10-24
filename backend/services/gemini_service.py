import json
import re
import base64
import logging
from typing import Optional, Dict, Any, List
import httpx
from ..config import GEMINI_API_KEY, DEFAULT_GEMINI_MODEL

logger = logging.getLogger(__name__)

def clean_json_text(text: str) -> str:
    """Strip markdown code fences and clean up text to extract valid JSON."""
    text = text.strip()
    # Strip ```json ... ``` or ``` ... ```
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    # Search for first '{' and last '}'
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        text = text[first_brace:last_brace + 1]
    return text.strip()

class GeminiMultimodalClient:
    def __init__(self, api_key: Optional[str] = None, model: str = DEFAULT_GEMINI_MODEL):
        self.api_key = api_key or GEMINI_API_KEY
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    async def generate_multimodal_json(
        self,
        prompt: str,
        image_bytes: bytes,
        mime_type: str = "image/jpeg",
        temperature: float = 0.2,
        system_instruction: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Call Gemini API with image and prompt, expecting a structured JSON response."""
        if not self.is_configured():
            logger.info("Gemini API key is not configured; using high-fidelity fallback.")
            return None

        endpoint = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        parts = [
            {"text": prompt},
            {
                "inline_data": {
                    "mime_type": mime_type,
                    "data": base64_image
                }
            }
        ]

        payload: Dict[str, Any] = {
            "contents": [
                {
                    "parts": parts
                }
            ],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": temperature,
                "maxOutputTokens": 3072
            }
        }

        if system_instruction:
            payload["system_instruction"] = {
                "parts": [{"text": system_instruction}]
            }

        headers = {
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=45.0) as client:
            try:
                response = await client.post(endpoint, json=payload, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        content_parts = candidates[0].get("content", {}).get("parts", [])
                        if content_parts:
                            raw_text = content_parts[0].get("text", "")
                            cleaned = clean_json_text(raw_text)
                            return json.loads(cleaned)
                else:
                    logger.warning(f"Gemini API returned status {response.status_code}: {response.text}")
                    return None
            except Exception as e:
                logger.error(f"Error calling Gemini multimodal API: {e}")
                return None

    async def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        system_instruction: str,
        temperature: float = 0.3
    ) -> Optional[str]:
        """Generate conversational response for construction chat."""
        if not self.is_configured():
            return None

        endpoint = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"

        contents = []
        for msg in messages:
            role = "user" if msg.get("role") == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg.get("content", "")}]
            })

        payload: Dict[str, Any] = {
            "contents": contents,
            "system_instruction": {
                "parts": [{"text": system_instruction}]
            },
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 2048
            }
        }

        async with httpx.AsyncClient(timeout=40.0) as client:
            try:
                response = await client.post(endpoint, json=payload, headers={"Content-Type": "application/json"})
                if response.status_code == 200:
                    data = response.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            return parts[0].get("text", "")
                return None
            except Exception as e:
                logger.error(f"Error in Gemini chat completion: {e}")
                return None
