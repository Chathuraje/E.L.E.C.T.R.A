from sqlalchemy import create_engine
from app.models import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from app.models.Users import DB_User
from app.libraries import config
from app.api.base.libraries.hashing import Hash
import os

#SQLALCHEMY_DATABASE_URL = "sqlite:///./app/electra.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5432/electra"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def create_db():
    Base.metadata.create_all(bind=engine)
    
    __create_superadmin_account()
        
        
        
def __create_superadmin_account():
    session = Session(bind=engine)
    existing_user = session.query(DB_User).filter_by(email=config.SUPER_ADMIN_EMAIL).first()
    if not existing_user:
        superadmin = DB_User(
            email=config.SUPER_ADMIN_EMAIL,
            password=Hash.bcrypt(config.SUPER_ADMIN_PASSWORD),
            first_name="Techincog",
            last_name=config.SUPER_ADMIN_FIRSTNAME,
            roles="superadmin",
        )
        session.add(superadmin)
        session.commit()
        session.refresh(superadmin)
            
        user_dir = os.path.join("app/storage", str(superadmin.id))
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        
        secret_dir = os.path.join(user_dir, "secrets")
        if not os.path.exists(secret_dir):
            os.makedirs(secret_dir)