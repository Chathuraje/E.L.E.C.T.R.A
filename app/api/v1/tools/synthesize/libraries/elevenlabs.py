# ::TODO:: Does not read inside the Documentation of the FastAPI if i use Post request.  Need to fix this.

from . import load_tools
main_tool_name, tool_data = load_tools("elevenlabs")


from app.libraries import secrets, config
from fastapi.responses import StreamingResponse
import io, os
from ..schemas import Audio
import requests
from app.api.base.libraries.users import get_user_storage_path
from fastapi import HTTPException
from app.api.base.libraries.storage import save_in_database, __random_name, create_user_sub_folders


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
    dir_name = await create_user_sub_folders(current_user.id, tool_data['system_folder_name'])
        
    filename = await __random_name()
    output_file_format = tool_data['output_file_format']
    
    filePath = f"{dir_name[0]}/{filename}{output_file_format}"
    
    await __synthesize(audio.text, filePath)
    
    file_description = f"({tool_data['sub_tool_name']}) - {audio.text}"
    with open(filePath, 'rb') as f:
        audio_file = f.read()
        real_name = f"{filename}{tool_data['output_file_format']}"
        await save_in_database(
            filename, 
            len(audio_file), 
            db, 
            current_user, 
            tool_data['mime_type'], 
            real_name, 
            tool_name=main_tool_name, 
            file_path=filePath, 
            file_description=file_description
        )
        
    return StreamingResponse(io.BytesIO(audio_file), media_type=tool_data['mime_type'])
    