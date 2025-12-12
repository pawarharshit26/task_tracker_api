from fastapi import FastAPI, Request
from app.apis.base import router
from app.apis.exceptions import BaseAPIException

app = FastAPI(title="Task Tracker API", description="Task Tracker API", version="1.0.0")

app.include_router(router)

@app.exception_handler(BaseAPIException)
def handle_base_api_exception(request: Request, e: BaseAPIException):
    return e.to_response()

@app.get("/")
def home():
    return {"message": "FastAPI Task Tracker Running!"}