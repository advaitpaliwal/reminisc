from fastapi import FastAPI
from reminisc.api.routes import router as memory_router

app = FastAPI(title="Reminisc API", summary="Memory for conversational LLMs")

app.include_router(memory_router, prefix="/api/v0", tags=["memory"])


@app.get("/")
async def root():
    return {"message": "Reminisc API"}
