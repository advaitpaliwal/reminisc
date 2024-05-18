from fastapi import FastAPI
from reminisc.api.routes import router as memory_router

app = FastAPI()

app.include_router(memory_router, prefix="/api/v0", tags=["memories"])


@app.get("/")
async def root():
    return {"message": "Reminisc API"}
