from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(title="Client Requests Bot API")

app.include_router(api_router, prefix="/api/v1")