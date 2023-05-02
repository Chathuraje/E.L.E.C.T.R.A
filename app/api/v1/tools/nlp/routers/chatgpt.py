# Tool: ChatGPT
main_tool_name = "nlp"
sub_tool_name = "ChatGPT"
description = "Chat with ChatGPT AI"

# Output file format
mime_type = "NA"
output_file_format = "NA"
system_folder_name = "NA"

# Usefull Information
use_db = False
use_storage = False

from fastapi import APIRouter
from ..libraries import chatgpt
from ..schemas import MetaData

router = APIRouter(
    prefix="/chatgpt",
    tags=["Chat GPT"]
)

@router.get("/")
async def ask(prompt: str):

    return await chatgpt.ask(prompt)


@router.post("/meta")
async def get_meta_data(meta: MetaData):
    
    return await chatgpt.get_meta_data(meta)
