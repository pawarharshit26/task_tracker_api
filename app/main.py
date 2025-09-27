from fastapi import APIRouter, FastAPI
from app.user.apis import user_router

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user_router)


@api_router.get("/health", tags=["Health"])
def read_root():
    return {"msg": "Hello, FastAPI + JWT!"}


app.include_router(api_router)
