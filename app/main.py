from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.base.services import static
from app.tasks.routers import tasks_router
from app.auth import auth_router

app = FastAPI()

app.mount("/static", static, name="static")
app.add_middleware(SessionMiddleware, secret_key="askljdhfgjlkasdjfldsanfasdfasdfadsf")
app.include_router(auth_router)
app.include_router(tasks_router)
