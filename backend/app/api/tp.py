from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from ..core.security import verify_jwt_token
from ..db.database import get_db
from ..db.models import TP, User
from ..schemas.tp import TPCreate, TP as TPSchema, TPList
from ..services.guacamole_service import get_guacamole_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tp", tags=["tp"])


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


@router.get("/{tp_id}/guacamole-access")
async def get_tp_guacamole_access(
    tp_id: int,
    token: str = Depends(verify_jwt_token),
    db: AsyncSession = Depends(get_db)
):
    """
    ✅ ACCÈS AUTOMATIQUE AU TP via Guacamole avec authentification CAS
    
    Lorsque l'utilisateur accède au TP, il est automatiquement authentifié
    et accède directement à la machine 100 (kali) sans passer par le login Guacamole.
    """
    try:
        # Vérifier que le TP existe
        result = await db.execute(select(TP).where(TP.id == tp_id))
        tp = result.scalar_one_or_none()
        
        if not tp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="TP not found"
            )
        
        # Récupérer l'utilisateur authentifié
        user = await db.get(User, int(token["sub"]))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
        # Obtenir le service Guacamole
        guac_service = get_guacamole_service()
        
        if not guac_service:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Service Guacamole non disponible"
            )
        
        logger.info(f"🎓 Accès TP {tp_id} avec Guacamole pour {user.cas_id}")
        
        # Générer l'URL d'accès direct au Guacamole (machine 100 - kali)
        guacamole_url = await guac_service.get_direct_access_url(
            username=user.cas_id,
            cas_username=user.cas_id,
            connection_id="c/kali"  # Machine 100 (kali)
        )
        
        if not guacamole_url:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Impossible de générer l'URL d'accès Guacamole"
            )
        
        logger.info(f"✅ Accès Guacamole direct pour TP {tp_id}: {user.cas_id}")
        
        return {
            "tp_id": tp_id,
            "tp_title": tp.title,
            "guacamole_url": guacamole_url,
            "username": user.cas_id,
            "vm_id": "100",
            "vm_name": "kali",
            "message": "Accès automatique avec authentification CAS"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'accès TP Guacamole: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
