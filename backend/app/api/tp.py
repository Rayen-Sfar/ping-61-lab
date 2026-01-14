from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.database import get_db

router = APIRouter()

# Mock data for TPs
mock_tps = [
    {
        "id": 1,
        "title": "TP 1: Introduction à Linux",
        "description": "Apprendre les commandes de base Linux",
        "instructions": "# Instructions TP 1\n\n1. Connectez-vous à la VM\n2. Exécutez `ls -la`\n3. Créez un fichier test.txt",
        "vm_status": "Stopped"
    }
]

@router.get("/")
async def get_tps(db: AsyncSession = Depends(get_db)):
    return mock_tps

@router.get("/{tp_id}")
async def get_tp(tp_id: int, db: AsyncSession = Depends(get_db)):
    tp = next((tp for tp in mock_tps if tp["id"] == tp_id), None)
    return tp 
