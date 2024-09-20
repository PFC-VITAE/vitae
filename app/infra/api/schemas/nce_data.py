from pydantic import BaseModel

class NCEData(BaseModel):
    code: str
    rank: str 
    profile: str
    knowledge: str
    application: str
    program: str