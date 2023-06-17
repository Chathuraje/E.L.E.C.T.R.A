main_tool = "nlp"
sub_tool_name = "ChatGPT"

from fastapi import APIRouter, Depends
from ..libraries import chatgpt
from ..schemas import MetaData
from .....base.schemas import User
from app.api.base.libraries import auth
from app.api.base.schemas import Roles


verify_role = auth.verify_role(accepted_roles=[Roles.user])
router = APIRouter(
    prefix="/chatgpt",
    tags=["Chat GPT"]
)

@router.get("/")
async def ask(
    prompt: str,
    current_user: User = Depends(verify_role)
):

    return await chatgpt.ask(prompt)
