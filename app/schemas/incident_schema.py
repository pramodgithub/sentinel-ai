from pydantic import BaseModel
from enum import Enum


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IncidentRequest(BaseModel):
    service: str
    description: str
    severity: Severity