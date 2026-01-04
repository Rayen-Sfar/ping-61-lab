from fastapi import FastAPI
from app.api import auth, tp, vm, guacamole

app = FastAPI(title="Lab on Demand API", version="1.0.0")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tp.router, prefix="/tp", tags=["tp"])
app.include_router(vm.router, prefix="/vm", tags=["vm"])
app.include_router(guacamole.router, prefix="/guacamole", tags=["guacamole"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Lab on Demand API"}
