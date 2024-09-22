from fastapi import APIRouter, Form, UploadFile, Depends
from typing import Annotated
from infra.storage.file_storage import FileStorage
from core.usecases.submit_document import SubmitDocument
from ..dependency import define_nce_dependency

router = APIRouter(
    prefix="/nce", tags=["NCE"], responses={404: {"description": "Not found"}}
)


@router.post("/submit")
async def submit_nce(
    file: UploadFile,
    pages: Annotated[str, Form(pattern="^\d+(?:-\d+)?$")],
    storage: Annotated[FileStorage, Depends()],
    usecase: Annotated[SubmitDocument, Depends(define_nce_dependency)],
):
    await storage.save(file)
    filepath = storage.path + file.filename
    dataframe = usecase.execute(filepath=filepath, pages=pages)
    return dataframe.to_dict(orient="records")
