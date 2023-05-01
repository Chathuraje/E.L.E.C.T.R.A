from sqlalchemy import create_engine
from app.models import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from app.models.Users import DB_User
from app.libraries import config
from app.api.base.libraries.hashing import Hash
import os
from app.libraries import config

LOCAL_STORAGE_LOCATION = config.LOCAL_STORAGE_LOCATION

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
        
        user_dir = os.path.join(LOCAL_STORAGE_LOCATION, str(superadmin.id))
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        
        sys_dir = os.path.join(user_dir, ".sys")
        if not os.path.exists(sys_dir):
            os.makedirs(sys_dir)
            
        screenshots_dir = os.path.join(sys_dir, "screenshots")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
            
        audios_dir = os.path.join(sys_dir, "audios")
        if not os.path.exists(audios_dir):
            os.makedirs(audios_dir)
            
        secrets_dir = os.path.join(sys_dir, "secrets")
        if not os.path.exists(secrets_dir):
            os.makedirs(secrets_dir)
            
        videos_dir = os.path.join(sys_dir, "videos")
        if not os.path.exists(videos_dir):
            os.makedirs(videos_dir)
            