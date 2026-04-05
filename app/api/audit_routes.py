from fastapi import APIRouter
from app.services.audit_query_service import AuditQueryService

router = APIRouter()

audit_service = AuditQueryService()


@router.get("/incident/{incident_id}/timeline")
def get_incident_timeline(incident_id: str):

    timeline = audit_service.get_incident_timeline(incident_id)

    return {
        "incident_id": incident_id,
        "timeline": timeline
    }