import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./labondemand.db")
    
    # CAS Configuration - URLs internes (pour backend) et externes (pour navigateur)
    cas_server_url: str = os.getenv("CAS_SERVER_URL", "http://cas:8080")
    cas_server_url_public: str = os.getenv("CAS_SERVER_URL_PUBLIC", "http://localhost:8888")
    cas_service_url: str = os.getenv("CAS_SERVICE_URL", "http://localhost:3000")
    
    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
    
    proxmox_host: str = os.getenv("PROXMOX_HOST", "proxmox.example.com")
    proxmox_user: str = os.getenv("PROXMOX_USER", "root@pam")
    proxmox_password: str = os.getenv("PROXMOX_PASSWORD", "password")
    proxmox_node: str = os.getenv("PROXMOX_NODE", "node1")
    guacamole_host: str = os.getenv("GUACAMOLE_HOST", "localhost")
    guacamole_port: int = int(os.getenv("GUACAMOLE_PORT", "8080"))
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")

settings = Settings()
