from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.database import get_db

router = APIRouter(prefix="/admin")

@router.get("/tp")
async def get_admin_tps(db: AsyncSession = Depends(get_db)):
    return []

@router.post("/tp")
async def create_tp(tp_data: dict, db: AsyncSession = Depends(get_db)):
    return {"message": "TP created"}

@router.get("/vm")
async def get_vms(db: AsyncSession = Depends(get_db)):
    return []