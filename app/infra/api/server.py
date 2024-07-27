from fastapi import FastAPI
from .routers import nce, vitae_extractor

app = FastAPI()

app.include_router(nce.router, prefix="/api")
app.include_router(vitae_extractor.router, prefix="/api")
 
@app.get("/")
async def root():
    return {"message": "Hello Vitae!"}
