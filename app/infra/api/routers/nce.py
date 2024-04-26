import aiofiles
from fastapi import APIRouter, Form, UploadFile
from typing import Annotated
from core.usecases.submit_nce import SubmitNCE

router = APIRouter(
    prefix="/nce", 
    tags=["NCE"], 
    dependencies=[],
    responses={404: {"description": "Not found"}}
)

@router.post("/submit")
async def submit_nce(upload_file: UploadFile, pages: Annotated[str, Form(pattern="^\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*$")]):
    async with aiofiles.open(f"app/infra/storage/{upload_file.filename}", "wb") as file:
        content = await upload_file.read()
        await file.write(content)
    
    return "success"
    