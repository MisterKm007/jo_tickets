from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Charger le fichier .env
load_dotenv()

# Lire l'URL de connexion
DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL =", DATABASE_URL)  # Pour déboguer

# Créer l'engine avec SSL (recommandé pour Supabase)
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def create_database():
    Base.metadata.create_all(bind=engine)
