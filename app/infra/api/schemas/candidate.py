from pydantic import BaseModel


class Candidate(BaseModel):
    rank: str
    qas_qms: str
    war_name: str
    full_name: str
