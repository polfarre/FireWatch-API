from fastapi import FastAPI
from app.routes import user_routes, incident_routes
from app.models import create_tables

app = FastAPI()

create_tables()

# Registrar las rutas
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(incident_routes.router, prefix="/incidents", tags=["incidents"])
