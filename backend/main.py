from fastapi import FastAPI
from auth import router as auth_router
from database import create_database
from billets import router as billet_router
from models import Billet 
from auth import router as auth_router




app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(billet_router)
app.include_router(auth_router)


@app.on_event("startup")
def startup():
    create_database()

@app.get("/")
def read_root():
    return {"message": "Bienvenue aux Jeux Olympiques 2024"}
