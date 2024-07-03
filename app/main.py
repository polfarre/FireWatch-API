from fastapi import FastAPI
from app.routes import user_routes, incident_routes
from app.models import create_tables

app = FastAPI()

create_tables()

app.include_router(user_routes.router, prefix="/usuarios", tags=["users"])
app.include_router(incident_routes.router, prefix="/incidentes", tags=["incidents"])
