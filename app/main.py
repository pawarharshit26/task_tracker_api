import structlog
from fastapi import FastAPI, Request

from app.apis.base import router
from app.apis.exceptions import BaseAPIException
from app.core.logging import setup_logging
from app.core.middlewares import RequestIDMiddleware, RequestLoggingMiddleware

setup_logging()

logger = structlog.get_logger(__name__)

app = FastAPI(title="Task Tracker API", description="Task Tracker API", version="1.0.0")

app.include_router(router)


@app.exception_handler(BaseAPIException)
def handle_base_api_exception(request: Request, e: BaseAPIException):
    return e.to_response()


app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RequestIDMiddleware)


@app.get("/")
def home():
    logger.info("Health Check", message="I am healthy")
    return {"message": "FastAPI Task Tracker Running!"}
