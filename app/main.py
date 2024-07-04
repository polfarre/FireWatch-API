from fastapi import FastAPI
from app.routes import incendio_routes, user_routes
from app.models import create_tables

app = FastAPI()

create_tables()

app.include_router(user_routes.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(incendio_routes.router, prefix="/incendios", tags=["Incendios"])
