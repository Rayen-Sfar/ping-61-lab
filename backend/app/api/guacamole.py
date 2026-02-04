"""
API endpoints pour l'intégration Guacamole avec authentification CAS
"""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from ..core.security import verify_jwt_token
from ..db.database import get_db
from ..db.models import User
from ..services.guacamole_service import get_guacamole_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/guacamole", tags=["guacamole"])


@router.get("/direct-access")
async def get_direct_guacamole_access(
    token: str = Depends(verify_jwt_token),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtenir l'accès direct à Guacamole (machine 100 - kali)
    L'utilisateur est automatiquement authentifié avec ses données CAS
    
    Retourne une URL vers laquelle rediriger pour l'accès direct
    """
    try:
        # Récupérer l'utilisateur actuel
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
        
        logger.info(f"🔓 Demande d'accès direct Guacamole pour {user.cas_id}")
        
        # Générer l'URL d'accès direct
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
        
        logger.info(f"✅ URL d'accès généré pour {user.cas_id}")
        
        return {
            "guacamole_url": guacamole_url,
            "username": user.cas_id,
            "connection": "kali",
            "vm_id": "100"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'accès direct Guacamole: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/list-connections")
async def list_guacamole_connections(
    token: str = Depends(verify_jwt_token)
):
    """
    Lister toutes les connexions Guacamole disponibles
    """
    try:
        guac_service = get_guacamole_service()
        
        if not guac_service:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Service Guacamole non disponible"
            )
        
        connections = await guac_service.list_connections()
        
        return {
            "connections": connections,
            "total": len(connections)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des connexions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
 
