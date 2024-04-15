from typing import List

from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from fastapi_users import fastapi_users, FastAPIUsers

from src.auth.base_config import auth_backend
from src.auth.manager import get_user_manager
from src.auth.schemas import UserCreate, UserRead
from src.database import User

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI(title="Petto")


@app.get("/user/{user_id}")
def get_user(user_id):
    return "not ready"


@app.post("/user/{user_id}")
def change_name(user_id: int, new_name):
    # fake_users[user_id] = new_name
    # return fake_users.get(user_id)
    return "not ready too"


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@app.get("/unprotected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, noname"
