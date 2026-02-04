from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, tp, vm, guacamole, admin
from app.db.database import engine, Base
from app.core.config import settings
from app.services.guacamole_service import GuacamoleService
from app.services import guacamole_service as gservice_module
import asyncio
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Lab on Demand API", version="1.0.0")

# Configuration CORS - STRICTE pour éviter les problèmes
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["Content-Type", "Authorization"],
    max_age=600,
)

@app.on_event("startup")
async def startup_event():
    # 1️⃣ Créer les tables de la base de données
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 2️⃣ Initialiser le service Guacamole
    logger.info("🚀 Initialisation du service Guacamole...")
    try:
        guac_service = GuacamoleService(
            api_url=settings.guacamole_api_url,
            public_url=settings.guacamole_public_url,
            guac_username=settings.guacamole_admin_username,
            guac_password=settings.guacamole_admin_password
        )
        
        # Authentifier auprès de Guacamole
        if await guac_service.authenticate():
            gservice_module.guacamole_service = guac_service
            logger.info("✅ Service Guacamole initialisé et authentifié")
        else:
            logger.warning("⚠️ Impossible d'authentifier le service Guacamole - les accès directs ne fonctionneront pas")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'initialisation de Guacamole: {str(e)}")

app.include_router(auth.router)
app.include_router(tp.router, prefix="/api")
app.include_router(vm.router, prefix="/api")
app.include_router(guacamole.router, prefix="/api")
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Lab on Demand API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

