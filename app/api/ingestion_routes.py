"""FastAPI routes for data ingestion."""

from fastapi import APIRouter, File, UploadFile
from typing import List

router = APIRouter(prefix="/ingestion", tags=["ingestion"])


@router.post("/documents")
async def ingest_documents(files: List[UploadFile] = File(...)):
    """Ingest documents for processing."""
    pass


@router.post("/incidents")
async def ingest_incidents(incidents: List[dict]):
    """Ingest incident data."""
    pass


@router.get("/status")
async def get_ingestion_status():
    """Get the status of ingestion tasks."""
    pass
