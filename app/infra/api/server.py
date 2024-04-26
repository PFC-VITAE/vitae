from fastapi import FastAPI
from .routers import nce

app = FastAPI()

app.include_router(nce.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello Vitae!"}
