from fastapi import FastAPI
from app.routers.v1.users import user_router

app = FastAPI(title="Task Tracker API")

app.include_router(user_router)
