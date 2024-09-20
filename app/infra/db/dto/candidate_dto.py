from dataclasses import dataclass, field
from typing import List, Dict
from bson import ObjectId
from datetime import datetime


@dataclass
class CursoDTO:
    name: str
    year_end: int
    school: str
    country: str
    modality: str


@dataclass
class CandidateDTO:
    _id: str
    rank: str
    qas_qms: str
    full_name: str
    war_name: str
    cpf: str
    birth_date: str
    promotion_date: str
    dgp_courses: List[CursoDTO] = field(default_factory=list)

    @classmethod
    def from_dict(cls, doc: Dict) -> "CandidateDTO":
        _id = (
            str(doc["_id"]) if isinstance(doc["_id"], ObjectId) else doc["_id"]["$oid"]
        )
        courses = [
            CursoDTO(
                name=course["Curso"],
                year_end=course["Ano Fim Curso"],
                school=course["Estab de Ensino"],
                country=course["País Curso"],
                modality=course["Modalidade Curso"],
            )
            for course in doc.get("Cursos", [])
        ]

        birth_date_formatted = datetime.strptime(
            doc["Data Nascimento"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%d/%m/%Y")

        return cls(
            _id=_id,
            rank=doc["Posto/ Grad"],
            qas_qms=doc["QAS-QMS"],
            full_name=doc["Nome"],
            war_name=doc["Nome Guerra"],
            cpf=doc["CPF"],
            birth_date=birth_date_formatted,
            promotion_date=doc["Dt Promocao"],
            dgp_courses=courses,
        )
