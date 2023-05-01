from fastapi import FastAPI
from .api import router
from .libraries import database
# 

app = FastAPI()
app.include_router(router)


database.create_db()

