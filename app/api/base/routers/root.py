from fastapi import APIRouter

router = APIRouter(
    tags=["Default"]
)

@router.get("/", include_in_schema=False)
async def root():
    return {"Hello": "World"}