# ::TODO:: Response only has one response, need to fix it


import os, random, string, time
from sqlalchemy.orm import Session
from app.libraries import database
from app.models.FileMetadata import DB_FileMetadata
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..schemas import FileMetadata
from fastapi.responses import StreamingResponse

get_db = database.get_db
location = "app/storage/"



async def __save_in_database(file, filename, file_size, db, current_user):

    file_metadata = DB_FileMetadata(
        id=filename,
        real_name=file.filename,
        file_size=file_size,
        file_type=file.content_type,
        # file_path=os.path.join(location, str(current_user.id), file.filename),
        owner_id=current_user.id,
        owner=current_user
    )
    db.add(file_metadata)
    db.commit()
    db.refresh(file_metadata)
    
    return filename
    
    
    
async def __save_in_storage(file, db, current_user):
    random_number = random.randint(1000, 9999)
    filename = str(round(time.time() * 1000)) + str(random_number)
    
    extension = os.path.splitext(file.filename)[1]
    file_path = os.path.join(location, str(current_user.id), str(f"{filename}"))
    
    with open(f"{file_path}{extension}", "wb") as f:
        while contents := file.file.read(1024 * 1024):
            f.write(contents)
        
    file_size = os.path.getsize(f"{file_path}{extension}")
    return filename, file_size



async def upload_file(files, current_user, db: Session = Depends(get_db)):
    file_metadata_list = []
    for file in files:
        filename, file_size = await __save_in_storage(file, db, current_user)
        await __save_in_database(file, filename, file_size, db, current_user)
        
        file_metadata_list.append(filename)
        
    return file_metadata_list
    
    
    
async def display_file_list(current_user, db):
    user_file_list = db.query(DB_FileMetadata).filter(DB_FileMetadata.owner_id == current_user.id).all()
    
    return user_file_list


async def download_file(file_id: str, current_user, db: Session = Depends(get_db)):
    file_metadata = db.query(DB_FileMetadata).filter(DB_FileMetadata.id == file_id).first()

    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")

    if file_metadata.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="User does not have permission to download file")

    file_path = os.path.join(location, str(current_user.id), str(file_metadata.id) + os.path.splitext(file_metadata.real_name)[1])

    file_stream = open(file_path, mode="rb")

    return StreamingResponse(file_stream, media_type=file_metadata.file_type, headers={"Content-Disposition": f"attachment; filename={file_metadata.real_name}"})



async def delete_file(file_id: str, current_user, db: Session = Depends(get_db)):
    file_metadata = db.query(DB_FileMetadata).filter(DB_FileMetadata.id == file_id).first()

    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")

    if file_metadata.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="User does not have permission to delete file")
    
    try:
        file_path = os.path.join(location, str(current_user.id), str(file_metadata.id) + os.path.splitext(file_metadata.real_name)[1])
        os.remove(file_path)
    except OSError as e:
        raise HTTPException(status_code=500, detail="File could not be deleted")
    
    db.delete(file_metadata)
    db.commit()
    
    return {"message": "File deleted successfully"}
