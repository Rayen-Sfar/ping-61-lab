 
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError, jwt
from datetime import datetime, timedelta
import logging

from ..core.config import settings
from ..core.security import create_access_token, verify_jwt_token
from ..services.cas_service import CASService
from ..db.database import get_db
from ..db.models import User
from ..schemas.auth import LoginResponse, UserSchema

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["authentication"])

# Initialiser le service CAS
cas_service = CASService(
    cas_server_url=settings.CAS_SERVER_URL,
    service_url=settings.BACKEND_URL
)

@router.get("/login")
async def cas_login():
    """
    ✅ Étape 1 : Redirection vers le serveur CAS
    
    Retourne l'URL de redirection vers CAS
    """
    cas_login_url = f"{cas_service.cas_server_url}/cas/login?service={cas_service.service_url}/api/auth/callback"
    return {"redirect_url": cas_login_url}

@router.get("/callback")
async def cas_callback(
    ticket: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """
    ✅ Étape 3 : Callback CAS (après authentification utilisateur)
    
    CAS redirige ici avec un ticket : /api/auth/callback?ticket=ST-xxxxx
    """
    
    if not ticket:
        raise HTTPException(status_code=400, detail="Ticket CAS manquant")
    
    # Valider le ticket auprès de CAS
    user_data = await cas_service.validate_ticket(ticket)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="❌ Authentification CAS échouée")
    
    username = user_data["username"]
    attributes = user_data.get("attributes", {})
    
    # Récupérer ou créer l'utilisateur en base locale
    stmt = select(User).where(User.cas_id == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        # ✅ Créer un nouvel utilisateur
        logger.info(f"✅ Nouvel utilisateur créé : {username}")
        user = User(
            cas_id=username,
            email=attributes.get("email", f"{username}@school.fr"),
            first_name=attributes.get("prenom", ""),
            last_name=attributes.get("nom", ""),
            role="student",  # Rôle par défaut
            auth_provider="cas",
            is_active=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    
    # Mettre à jour last_login
    user.last_login = datetime.utcnow()
    await db.commit()
    
    # Générer JWT
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=str(user.id),
        username=user.cas_id,
        role=user.role
    )

@router.get("/me", response_model=UserSchema)
async def get_current_user(
    token: str = Depends(verify_jwt_token),
    db: AsyncSession = Depends(get_db)
):
    """Récupérer l'utilisateur actuel"""
    
    user = await db.get(User, token["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    return user

@router.post("/logout")
async def logout():
    """✅ Déconnexion (côté frontend : supprimer JWT + token)"""
    return {"message": "Déconnexion réussie"}