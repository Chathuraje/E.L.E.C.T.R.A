main_tool = "nlp"
sub_tool_name = "ChatGPT"

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
