from fastapi import APIRouter, Depends
from typing import Annotated
from core.usecases.submit_document import SubmitDocument
from ..dependency import define_ranking_dependancy
from ..schemas.nce_data import NCEData
from ..schemas.candidate import Candidate

router = APIRouter(
    prefix="/ranking", tags=["Ranking"], responses={404: {"description": "Not found"}}
)


@router.post("/list_best_candidates", response_model=list[Candidate])
async def list_best_candidates(
    nce: NCEData, usecase: Annotated[SubmitDocument, Depends(define_ranking_dependancy)]
):
    return usecase.execute(nce)
