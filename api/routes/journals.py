from fastapi import APIRouter, Query
from typing import List, Dict, Any
from filing_cabinet import loader

router = APIRouter()

@router.get("/journals/latest", response_model=List[Dict[str, Any]])
def get_latest_journals(n: int = Query(5, ge=1, le=50)) -> List[Dict[str, Any]]:
    """
    Returns the latest n journal entries.
    """
    return loader.get_latest_entries("journals", n)
from fastapi import APIRouter, Query
from typing import List, Dict, Any
from filing_cabinet import loader

router = APIRouter()

@router.get("/journals/latest", response_model=List[Dict[str, Any]])
def get_latest_journals(n: int = Query(5, ge=1, le=50)) -> List[Dict[str, Any]]:
    """
    Returns the latest n journal entries.
    """
    return loader.get_latest_entries("journals", n)
