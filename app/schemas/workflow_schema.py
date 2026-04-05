"""Pydantic schemas for workflow data."""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class WorkflowBase(BaseModel):
    """Base workflow schema."""
    name: str
    description: Optional[str] = None
    steps: List[Dict[str, Any]]


class WorkflowCreate(WorkflowBase):
    """Schema for creating workflows."""
    pass


class WorkflowResponse(WorkflowBase):
    """Schema for workflow responses."""
    id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class WorkflowExecution(BaseModel):
    """Schema for workflow execution."""
    workflow_id: str
    incident_id: str
    status: str
    started_at: str
    completed_at: Optional[str] = None
    results: Optional[Dict[str, Any]] = None
