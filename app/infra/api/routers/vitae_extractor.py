from fastapi import APIRouter, Depends
from typing import Annotated
from core.usecases.consolidate_candidate_data import ConsolidateCandidateData
from ..dependency import define_candidate_dependency

router = APIRouter(
    prefix="/extractor",
    tags=["Vitae Extractor"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_data")
def consolidate_data(
    usecase: Annotated[ConsolidateCandidateData, Depends(define_candidate_dependency)]
):

    return usecase.execute()
