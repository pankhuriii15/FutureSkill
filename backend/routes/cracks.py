from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from ..schemas.crack_schemas import CrackDiagnosisResponse
from ..services.crack_analyzer import diagnose_crack_defect

router = APIRouter(prefix="/api", tags=["Crack Diagnostics & Structural Integrity"])

@router.post(
    "/diagnose-crack",
    response_model=CrackDiagnosisResponse,
    summary="Diagnose concrete and wall crack defect types, width, root causes and engineering repairs"
)
async def diagnose_crack_endpoint(
    file: UploadFile = File(..., description="Concrete, masonry, or wall defect image (JPEG/PNG)"),
    notes: Optional[str] = Form(None, description="Optional structural location or observations"),
    api_key: Optional[str] = Form(None, description="Optional client-provided Gemini API key")
):
    """
    Multimodal endpoint to classify crack defects (Hairline, Settlement, Structural Shear, Thermal Expansion, Spalling)
    with estimated crack width (mm), root causes, recommended engineering repairs, and urgency.
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
        if len(contents) > 20 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Image file size exceeds maximum 20MB limit."
            )

        diagnosis_result = await diagnose_crack_defect(
            image_bytes=contents,
            mime_type=file.content_type,
            notes=notes,
            api_key=api_key
        )
        return diagnosis_result
    except HTTPException:
        raise
    except ValueError as val_err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(val_err))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Diagnosis failed: {str(e)}")
