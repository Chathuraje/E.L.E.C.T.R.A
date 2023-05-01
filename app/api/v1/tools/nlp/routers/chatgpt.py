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
