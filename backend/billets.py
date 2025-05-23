from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Billet
from schemas import BilletCreate
import uuid
import random
import string
from utils import get_current_user

router = APIRouter(prefix="/billets", tags=["Billets"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@router.post("/")
def create_billet(billet: BilletCreate, db: Session = Depends(get_db)):
    code = generate_code()
    while db.query(Billet).filter_by(code=code).first():
        code = generate_code()

    new_billet = Billet(
        type=billet.type,
        client_name=billet.client_name,
        email=billet.email,
        code=code
    )
    db.add(new_billet)
    db.commit()
    db.refresh(new_billet)
    return {
        "id": str(new_billet.id),
        "code": new_billet.code,
        "type": new_billet.type,
        "created_at": new_billet.created_at
    }

@router.get("/protected")
def protected_route(current_user = Depends(get_current_user)):
    return {"message": f"Bienvenue {current_user.username}, tu es bien authentifié ✅"}
