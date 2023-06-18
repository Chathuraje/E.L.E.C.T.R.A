from sqlalchemy import create_engine
from app.models import Base
from sqlalchemy.orm import sessionmaker
from app.libraries import config
from . import super_admin

LOCAL_STORAGE_LOCATION = config.LOCAL_STORAGE_LOCATION

#SQLALCHEMY_DATABASE_URL = "sqlite:///./app/electra.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/electra"

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
    super_admin.create_superadmin_account(engine)
        
            