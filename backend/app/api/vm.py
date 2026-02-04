from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.database import get_db
import asyncio
import logging

router = APIRouter(prefix="/vm", tags=["vm"])

logger = logging.getLogger(__name__)

@router.post("/start/{tp_id}")
async def start_vm(tp_id: int, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    # Mock starting VM
    logger.info(f"Starting VM for TP {tp_id}")
    
    # Programmer l'arrêt automatique après 2 heures (contrainte RAM 16Go)
    background_tasks.add_task(stop_vm_after_timeout, tp_id, timeout_hours=2)
    
    return {"guacamole_url": "http://localhost:8088/guacamole/#/client/1/"}

@router.post("/stop/{tp_id}")
async def stop_vm(tp_id: int, db: AsyncSession = Depends(get_db)):
    # Mock stopping VM
    logger.info(f"Stopping VM for TP {tp_id}")
    return {"message": "VM stopped"}

async def stop_vm_after_timeout(tp_id: int, timeout_hours: int = 2):
    """Tâche de fond pour arrêter automatiquement la VM après un délai"""
    seconds = timeout_hours * 3600
    logger.info(f"VM {tp_id} will auto-stop in {timeout_hours} hours ({seconds} seconds)")
    
    await asyncio.sleep(seconds)
    
    # Ici, appeler la logique d'arrêt de VM
    logger.info(f"Auto-stopping VM for TP {tp_id} after {timeout_hours} hours")
    # Dans un vrai environnement, appeler l'API Proxmox pour arrêter la VM 
