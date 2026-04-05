"""Pydantic schemas for evaluation data."""

from pydantic import BaseModel
from typing import Optional, Dict, Any


class EvaluationBase(BaseModel):
    """Base evaluation schema."""
    incident_id: str
    resolved: bool
    root_cause_confirmed: bool
    confidence_level: float = 0.0


class EvaluationCreate(EvaluationBase):
    """Schema for creating evaluations."""
    findings: Optional[Dict[str, Any]] = None
    recommendations: Optional[Dict[str, Any]] = None


class EvaluationResponse(EvaluationCreate):
    """Schema for evaluation responses."""
    id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
