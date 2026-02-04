import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./labondemand.db")
    
    # CAS Configuration - URLs internes (pour backend) et externes (pour navigateur)
    cas_server_url: str = os.getenv("CAS_SERVER_URL", "http://cas:8080")
    cas_server_url_public: str = os.getenv("CAS_SERVER_URL_PUBLIC", "http://localhost:8888")
    cas_service_url: str = os.getenv("CAS_SERVICE_URL", "http://localhost:3000")
    
    # JWT - Names must match security.py usage (lowercase)
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    jwt_expire_minutes: int = int(os.getenv("JWT_EXPIRE_MINUTES", "480"))  # 8 heures au lieu de 15 minutes
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    
    # Guacamole Configuration
    # URL utilisée par le backend pour appeler l'API Guacamole (résolution interne dans Docker)
    guacamole_api_url: str = os.getenv("GUACAMOLE_API_URL", os.getenv("GUACAMOLE_URL", "http://guacamole:8080/guacamole"))
    # URL publique renvoyée au navigateur; doit être résolue depuis le poste client (ex: http://10.3.0.76:8080/guacamole)
    guacamole_public_url: str = os.getenv("GUACAMOLE_PUBLIC_URL", os.getenv("GUACAMOLE_URL", "http://localhost:8088/guacamole"))
    guacamole_admin_username: str = os.getenv("GUACAMOLE_ADMIN_USERNAME", "guacadmin")
    guacamole_admin_password: str = os.getenv("GUACAMOLE_ADMIN_PASSWORD", "guacadmin")
    # Rétro-compatibilité: guacamole_url pointe vers l'API interne
    guacamole_url: str = guacamole_api_url
    
    # Proxmox Configuration
    proxmox_host: str = os.getenv("PROXMOX_HOST", "proxmox.example.com")
    proxmox_user: str = os.getenv("PROXMOX_USER", "root@pam")
    proxmox_password: str = os.getenv("PROXMOX_PASSWORD", "password")
    proxmox_node: str = os.getenv("PROXMOX_NODE", "node1")

    # Sécurité / Rôles
    # Liste CSV des groupes LDAP qui doivent être considérés comme administrateurs
    admin_groups: str = os.getenv("ADMIN_GROUPS", "admin,admins,teacher,teachers")

settings = Settings()

