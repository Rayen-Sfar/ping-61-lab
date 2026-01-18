 
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
    cas_server_url=settings.cas_server_url,  # URL interne pour validation
    service_url=settings.cas_service_url  # URL de base du frontend
)

from pydantic import BaseModel

class LDAPLoginRequest(BaseModel):
    username: str
    password: str

@router.post("/ldap-login")
async def ldap_login(
    request: LDAPLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    ✅ Authentification directe LDAP (sans redirection CAS)
    """
    logger.info(f"🔑 Tentative de connexion LDAP pour: {request.username}")
    
    # Valider contre LDAP via le service CAS
    import httpx
    try:
        # Appeler le endpoint LDAP du serveur CAS
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.cas_server_url}/ldap/authenticate",
                json={"username": request.username, "password": request.password},
                timeout=10
            )
        
        if response.status_code != 200:
            logger.warning(f"❌ Authentification LDAP échouée pour {request.username}")
            raise HTTPException(status_code=401, detail="Identifiants invalides")
        
        user_data = response.json()
        logger.info(f"✅ Authentification LDAP réussie pour {request.username}")
        
    except httpx.RequestError as e:
        logger.error(f"❌ Erreur de connexion au serveur LDAP: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
    
    # Récupérer ou créer l'utilisateur en base locale
    stmt = select(User).where(User.cas_id == request.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        logger.info(f"✅ Nouvel utilisateur créé : {request.username}")
        user = User(
            cas_id=request.username,
            email=user_data.get("mail", f"{request.username}@esigelec.fr"),
            first_name=user_data.get("givenName", ""),
            last_name=user_data.get("sn", ""),
            role="student",
            auth_provider="ldap",
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
    
    logger.info(f"✅ JWT généré pour {request.username}")
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=str(user.id),
        username=user.cas_id,
        role=user.role
    )

@router.get("/login")
async def cas_login():
    """
    ✅ Étape 1 : Redirection vers le serveur CAS
    
    Retourne l'URL de redirection vers CAS (URL publique pour le navigateur)
    """
    cas_login_url = f"{settings.cas_server_url_public}/cas/login?service={settings.cas_service_url}"
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
    
    logger.info(f"🎫 Callback CAS reçu avec ticket: {ticket}")
    
    if not ticket:
        raise HTTPException(status_code=400, detail="Ticket CAS manquant")
    
    # Valider le ticket auprès de CAS
    logger.info(f"🔍 Validation du ticket auprès de CAS: {settings.cas_server_url}")
    user_data = await cas_service.validate_ticket(ticket)
    
    if not user_data:
        logger.error("❌ Validation CAS échouée - ticket invalide ou expiré")
        # Rediriger vers la page de login avec erreur
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=f"{settings.cas_service_url}/?error=auth_failed")
    
    logger.info(f"✅ Validation CAS réussie pour: {user_data.get('username')}")
    
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
    
    logger.info(f"✅ JWT généré pour {username}")
    
    # Rediriger vers le frontend avec le token
    from fastapi.responses import RedirectResponse
    from urllib.parse import urlencode
    
    # Paramètres à passer au frontend
    params = {
        'token': access_token,
        'user_id': str(user.id),
        'username': user.cas_id,
        'role': user.role
    }
    
    # Déterminer la page de redirection selon le rôle
    if user.role in ['teacher', 'admin']:
        redirect_url = f"{settings.cas_service_url}/admin?{urlencode(params)}"
    else:
        redirect_url = f"{settings.cas_service_url}/dashboard?{urlencode(params)}"
    
    logger.info(f"✅ Redirection vers: {redirect_url}")
    return RedirectResponse(url=redirect_url)

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