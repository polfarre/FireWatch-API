from fastapi import FastAPI
from app.routes import incendio_routes, user_routes
from fastapi.middleware.cors import CORSMiddleware
from app.models import create_tables
import os

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.getenv("TESTING") != "True":
    create_tables()

app.include_router(user_routes.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(incendio_routes.router, prefix="/incendios", tags=["Incendios"])
