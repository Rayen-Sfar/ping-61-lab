from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, tp, vm, guacamole, admin
from app.db.database import engine, Base
import asyncio

app = FastAPI(title="Lab on Demand API", version="1.0.0")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:5173"],  # Autoriser le frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)
app.include_router(tp.router, prefix="/tp")
app.include_router(vm.router, prefix="/vm")
app.include_router(guacamole.router, prefix="/guacamole")
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Lab on Demand API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
