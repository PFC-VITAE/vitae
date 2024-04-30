from dataclasses import dataclass, field
from typing import List, Dict
from bson import ObjectId
from datetime import datetime

@dataclass
class CursoDTO:
    nome: str
    ano_fim: int
    estab_ensino: str
    pais_curso: str
    modalidade: str

@dataclass
class CandidateDTO:
    _id: str
    posto_grad: str
    qas_qms: str
    nome: str
    nome_guerra: str
    cpf: str
    data_nascimento: str
    ano_turma: int
    dt_promocao: str
    cursos: List[CursoDTO] = field(default_factory=list)

    @classmethod
    def from_dict(cls, doc: Dict) -> 'CandidateDTO':
        _id = str(doc["_id"]) if isinstance(doc["_id"], ObjectId) else doc["_id"]["$oid"]
        cursos = [CursoDTO(nome=curso["Curso"], 
                        ano_fim=curso["Ano Fim Curso"], 
                        estab_ensino=curso["Estab de Ensino"], 
                        pais_curso=curso["País Curso"], 
                        modalidade=curso["Modalidade Curso"]) 
                for curso in doc.get("Cursos", [])]
        
        data_nascimento_formatted = datetime.strptime(doc["Data Nascimento"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d/%m/%Y")

        return cls(
            _id=_id,
            posto_grad=doc["Posto/ Grad"],
            qas_qms=doc["QAS-QMS"],
            nome=doc["Nome"],
            nome_guerra=doc["Nome Guerra"],
            cpf=doc["CPF"],
            data_nascimento=data_nascimento_formatted,
            ano_turma=doc["Ano Turma"],
            dt_promocao=doc["Dt Promocao"],
            cursos=cursos
        )
