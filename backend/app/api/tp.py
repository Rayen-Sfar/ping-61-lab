from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db.database import get_db
from ..db.models import TP
from ..schemas.tp import TPCreate, TP as TPSchema, TPList

router = APIRouter()


@router.post("/", response_model=TPSchema, status_code=status.HTTP_201_CREATED)
async def create_tp(tp_data: TPCreate, db: AsyncSession = Depends(get_db)):
    """Créer un nouveau TP"""
    try:
        db_tp = TP(
            title=tp_data.title,
            description=tp_data.description,
            instructions=tp_data.instructions,
            difficulty=tp_data.difficulty,
            duration=tp_data.duration,
            vm_type=tp_data.vm_type,
            status=tp_data.status,
            created_by=tp_data.created_by
        )
        db.add(db_tp)
        await db.commit()
        await db.refresh(db_tp)
        return db_tp
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=list[TPList])
async def get_tps(db: AsyncSession = Depends(get_db)):
    """Récupérer tous les TPs"""
    try:
        result = await db.execute(select(TP))
        tps = result.scalars().all()
        return tps
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{tp_id}", response_model=TPSchema)
async def get_tp(tp_id: int, db: AsyncSession = Depends(get_db)):
    """Récupérer un TP par ID"""
    try:
        result = await db.execute(select(TP).where(TP.id == tp_id))
        tp = result.scalar_one_or_none()
        if not tp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TP not found")
        return tp
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{tp_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tp(tp_id: int, db: AsyncSession = Depends(get_db)):
    """Supprimer un TP"""
    try:
        result = await db.execute(select(TP).where(TP.id == tp_id))
        tp = result.scalar_one_or_none()
        if not tp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TP not found")
        await db.delete(tp)
        await db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 
