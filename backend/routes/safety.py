from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from ..schemas.safety_schemas import SafetyAuditResponse
from ..services.safety_analyzer import analyze_site_safety

router = APIRouter(prefix="/api", tags=["Site Safety & PPE Audit"])

@router.post(
    "/audit-safety",
    response_model=SafetyAuditResponse,
    summary="Audit construction site photo for PPE compliance and site hazards"
)
async def audit_safety_endpoint(
    file: UploadFile = File(..., description="Construction site image (JPEG/PNG)"),
    notes: Optional[str] = Form(None, description="Optional inspector notes / context"),
    api_key: Optional[str] = Form(None, description="Optional client-provided Gemini API key")
):
    """
    Multimodal endpoint to inspect site photos for PPE compliance (helmets, high-vis vests,
    safety boots, harnesses) under OSHA 1926 and IS 456 / IS 2925 standards.
    """
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be a valid image format (JPEG, PNG, WebP)"
        )

    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty (0 bytes)."
            )
        if len(contents) > 20 * 1024 * 1024:  # 20MB limit
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Image file size exceeds maximum 20MB limit."
            )

        audit_result = await analyze_site_safety(
            image_bytes=contents,
            mime_type=file.content_type,
            notes=notes,
            api_key=api_key
        )
        return audit_result
    except HTTPException:
        raise
    except ValueError as val_err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(val_err))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Analysis failed: {str(e)}")
