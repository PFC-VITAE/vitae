from pydantic import BaseModel, Field


class NCEData(BaseModel):
    application: str = Field(..., alias="Aplicação")
    knowledge: str = Field(..., alias="Conhecimento Específico")
    code: str = Field(..., alias="NCE (Prio)")
    profile: str = Field(..., alias="Perfil")
    rank: str = Field(..., alias="Posto")
