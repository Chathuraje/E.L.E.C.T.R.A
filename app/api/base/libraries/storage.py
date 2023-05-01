# ::TODO:: Response only has one response, need to fix it

import os, random, string, time
from sqlalchemy.orm import Session
from app.libraries import database
from app.models.FileMetadata import DB_FileMetadata
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..schemas import FileMetadata
from fastapi.responses import StreamingResponse
from app.libraries import config

get_db = database.get_db
LOCAL_STORAGE_LOCATION = config.LOCAL_STORAGE_LOCATION



async def save_in_database(filename, file_size, db, current_user, content_type, real_name, tool_name, file_description=None):

    file_metadata = DB_FileMetadata(
        id=filename,
        real_name=real_name,
        file_size=file_size,
        tool_name=tool_name,
        file_type=content_type,
        # file_path=os.path.join(location, str(current_user.id), file.filename),
        file_description=file_description,
        owner_id=current_user.id,
        owner=current_user
    )
    db.add(file_metadata)
    db.commit()
    db.refresh(file_metadata)
    
    return filename


async def __random_name():
    random_number = random.randint(1000, 9999)
    filename = str(round(time.time() * 1000)) + str(random_number)
    
    return filename    
    
    
async def save_in_storage(file, db, current_user):
    
    filename = await __random_name()
    extension = os.path.splitext(file.filename)[1]
    file_path = os.path.join(LOCAL_STORAGE_LOCATION, str(current_user.id), str(f"{filename}"))
    
    with open(f"{file_path}{extension}", "wb") as f:
        while contents := file.file.read(1024 * 1024):
            f.write(contents)
        
    file_size = os.path.getsize(f"{file_path}{extension}")
    return filename, file_size



async def upload_file(files, current_user, db, tool_name):
    file_metadata_list = []
    for file in files:
        filename, file_size = await save_in_storage(file, db, current_user)
        await save_in_database(filename, file_size, db, current_user, file.content_type, file.filename, tool_name=tool_name)
        
        file_metadata_list.append(filename)
        
    return file_metadata_list
    
    
    
async def display_file_list(current_user, db, tool_name):
    user_file_list = db.query(DB_FileMetadata).filter(
        (DB_FileMetadata.owner_id == current_user.id) &
        (DB_FileMetadata.tool_name == tool_name)
    ).all()
    
    return user_file_list


async def download_file(file_id: str, current_user, tool_name, db: Session = Depends(get_db)):
    file_metadata = db.query(DB_FileMetadata).filter(
        (DB_FileMetadata.owner_id == current_user.id) &
        (DB_FileMetadata.tool_name == tool_name)
    ).first()

    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")

    if file_metadata.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="User does not have permission to download file")

    file_path = os.path.join(LOCAL_STORAGE_LOCATION, str(current_user.id), str(file_metadata.id) + os.path.splitext(file_metadata.real_name)[1])

    file_stream = open(file_path, mode="rb")

    return StreamingResponse(file_stream, media_type=file_metadata.file_type, headers={"Content-Disposition": f"attachment; filename={file_metadata.real_name}"})



async def delete_file(file_id: str, current_user, tool_name, db: Session = Depends(get_db)):
    file_metadata = db.query(DB_FileMetadata).filter(
        (DB_FileMetadata.owner_id == current_user.id) &
        (DB_FileMetadata.tool_name == tool_name)
    ).first()

    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")

    if file_metadata.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="User does not have permission to delete file")
    
    try:
        file_path = os.path.join(LOCAL_STORAGE_LOCATION, str(current_user.id), str(file_metadata.id) + os.path.splitext(file_metadata.real_name)[1])
        os.remove(file_path)
    except OSError as e:
        raise HTTPException(status_code=500, detail="File could not be deleted")
    
    db.delete(file_metadata)
    db.commit()
    
    return {"message": "File deleted successfully"}
