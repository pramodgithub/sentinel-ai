from fastapi import FastAPI
from app.api import incident_routes
from app.api import audit_routes

app = FastAPI(
    title="Sentinel AI",
    description="Autonomous Incident Resolution Agent"
)

app.include_router(incident_routes.router)
app.include_router(audit_routes.router)


@app.get("/health")
def health():
    return {"status": "ok"}