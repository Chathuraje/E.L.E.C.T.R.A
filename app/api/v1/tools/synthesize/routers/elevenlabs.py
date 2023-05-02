
# Tool: Synthesize
main_tool_name = "synthesize"
sub_tool_name = "elevenlabs"
description = "Synthesize audio using ElevenLabs API"

# Output file format
mime_type = "audio/mpeg"
output_file_format = ".mp3"

# Usefull Information
use_db = True
use_storage = True
storage = "audios"

from fastapi import APIRouter, Response, Depends
from ..libraries import elevenlabs
from ..schemas import Audio
from app.api.base.libraries import auth
from app.api.base.schemas import Roles
from app.libraries import database
from .....base.schemas import User
from sqlalchemy.orm import Session

get_db = database.get_db
verify_role = auth.verify_role(accepted_roles=[Roles.user])

router = APIRouter()

@router.post("/elevenlabs")
async def generate_audio(
    audio: Audio,
    current_user: User = Depends(verify_role),
    db: Session = Depends(get_db)
):
    
    return await elevenlabs.generate_audio(audio, current_user, db)
