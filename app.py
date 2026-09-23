from fastapi import FastAPI

from routers.keys import router as keys_router


app = FastAPI(
    title="KeyPilot API",
    version="0.1.0",
    description="Backend zur Verwaltung von Schlüsseln, Räumen und Ausleihen.",
)

@app.get("/")
def read_root():
    return {"name": "KeyPilot API", "status": "ok"}


app.include_router(keys_router)
