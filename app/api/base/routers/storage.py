from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from app.api.base.libraries import auth
from app.api.base.schemas import Roles
from ..libraries import storage
from app.libraries import database
from sqlalchemy.orm import Session
from ..schemas import User
from typing import List
from ..schemas import FileMetadata


get_db = database.get_db
verify_role = auth.verify_role(accepted_roles=[Roles.user])
# tool_name="storage"

router = APIRouter(
    prefix="/storage",
    tags=["Storage"]
)

@router.post("/")
async def display_file_list( 
    tool_name: str = "storage",
    current_user: User = Depends(verify_role),
    db: Session = Depends(get_db)
):
    return await storage.display_file_list(current_user, db, tool_name)

@router.post("/upload")
async def upload_file(
    files: List[UploadFile] = File(...), 
    current_user: User = Depends(verify_role), 
    db: Session = Depends(get_db)
):
    
    return await storage.upload_file(files, current_user, db, tool_name="storage")
    

@router.post("/{file_id}")
async def download_file(
        file_id: str, 
        tool_name: str = "storage",
        current_user: User = Depends(verify_role), 
        db: Session = Depends(get_db)
    ):
    
    return await storage.download_file(file_id, current_user, tool_name, db)


@router.delete("/{file_id}")
async def delete_file(
    file_id: str, 
    tool_name: str = "storage",
    current_user: User = Depends(verify_role), 
    db: Session = Depends(get_db)
):
    
    return await storage.delete_file(file_id, current_user, tool_name, db)


