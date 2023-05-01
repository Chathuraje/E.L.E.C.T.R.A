# Tool: Synthesize
tool_name = "synthesize/elevenlabs.py"
description = "Synthesize audio using ElevenLabs API"

# Output file format
mime_type = "audio/mpeg"
output_file_format = ".mp3"

# Usefull Information
use_db = True
use_storage = True
storage = "audios"


# ::TODO:: Does not read inside the Documentation of the FastAPI if i use Post request.  Need to fix this.

from app.libraries import secrets, config
from fastapi.responses import StreamingResponse
import io
from ..schemas import Audio
import requests
from app.api.base.libraries.users import get_user_storage_path
from fastapi import HTTPException
from app.api.base.libraries.storage import save_in_database, __random_name


async def __synthesize(text: str, filePath: str):
    voice_id = config.VOICE_ID
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
    payload = {
        'text': text,
        'voice_settings': {
            'stability': 0,
            'similarity_boost': 0
        }
    }

    headers = {
        'accept': 'audio/mpeg',
        'Content-Type': 'application/json',
        'xi-api-key': secrets.TEXT_TO_SPEECH_API_KEY,
    }
        
    response = requests.post(url, json=payload, headers=headers)
            
    if response.status_code == 200:
        with open(filePath, 'wb') as f:
            f.write(response.content)
    else:
        raise HTTPException(status_code=400, detail=f"Error in generating audio {response.status_code} : {response.text}")
            
               
                
async def generate_audio(audio: Audio, current_user, db):
    filename = await __random_name()
    
    user_path = await get_user_storage_path(current_user, system=True)
    filePath = f"{user_path}/{storage}/{filename}{output_file_format}"
    
    await __synthesize(audio.text, filePath)
    
    file_description = f"Generated Audio - {audio.text}"
    with open(filePath, 'rb') as f:
        audio_file = f.read()
        await save_in_database(filename, len(audio_file), db, current_user, mime_type, filename, tool_name=tool_name, file_description=file_description)
        
    return StreamingResponse(io.BytesIO(audio_file), media_type=mime_type)
    