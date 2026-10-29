from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth_router import router as auth_router
from app.routers.provider_router import router as provider_router


from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database.session import engine


app = FastAPI(
    title="Photo Platform API",
    description="API de gestion de prestations photographiques",
    version="0.1.0"
)

app.include_router(auth_router)
app.include_router(provider_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Bienvenue sur Photo Platform API",
        "version": "0.1.0"
    }


@app.get("/api/v1/health")
def health():
    return {
        "status": "ok",
        "service": "photo-platform-api"
    }

@app.get("/api/v1/health/database")
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected"
        }

    except SQLAlchemyError:
        return {
            "status": "error",
            "database": "disconnected"
        }