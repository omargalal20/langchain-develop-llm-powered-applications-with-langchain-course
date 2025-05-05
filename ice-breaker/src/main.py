from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from config.logger import setup_logging
from config.settings import get_settings
from presentation.routers import health
from presentation.routers.v1 import ice_breaker

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/public", StaticFiles(directory="public"), name="public")


@app.get("/")
async def read_index():
    return FileResponse('public/index.html')


app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(ice_breaker.router, prefix="/api/v1", tags=["Ice Breaker"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
