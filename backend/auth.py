from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserCreate
from passlib.context import CryptContext
import uuid
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentification"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str):
    return pwd_context.hash(password)

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Vérifie si l'email existe déjà
    existing_user = db.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    new_user = User(
        id=uuid.uuid4(),
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
        created_at=datetime.utcnow()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Inscription réussie", "id": str(new_user.id)}


from schemas import UserLogin
from utils import SECRET_KEY, ALGORITHM
from jose import jwt

from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

@router.post("/login")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_login.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    if not pwd_context.verify(user_login.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")

    payload = {
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=60)  # expiration du token
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
