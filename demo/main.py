from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from .items import router as user_router
from .sleeps import router as sleep_router

app = FastAPI()
app.include_router(user_router)
app.include_router(sleep_router)


@app.get("/healthz")
async def get_health():
    return {"msg": "Healthy"}
