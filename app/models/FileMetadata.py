from sqlalchemy import Column, DateTime, String, Column, Integer, String, ForeignKey
from app.models import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from sqlalchemy.dialects.postgresql import UUID

class DB_FileMetadata(Base):
    __tablename__ = "file_metadata"
    
    id = Column(String, primary_key=True, index=True)
    real_name = Column(String)
    file_size = Column(Integer)
    file_type = Column(String)
    tool_name = Column(String)
    # file_path = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    owner = relationship("DB_User", backref="files")