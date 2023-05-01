from sqlalchemy import Column, DateTime, String, Boolean, Enum, Integer
from app.models import Base
from sqlalchemy.sql import func
import uuid
from sqlalchemy.dialects.postgresql import UUID

class DB_User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=str(uuid.uuid4()), index=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String, nullable=False)
    roles = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    