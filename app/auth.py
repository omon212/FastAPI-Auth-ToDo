from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.databace import User, get_db, SessionLocal
from app.base.services import templates

SECRET_KEY = "aasdfjkahsdfasdasdfadsfasdfasdflkjlkajsdfasdf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_router = APIRouter()


async def verify_pass(plain_pass: str, hashed_pass: str) -> bool:
    try:
        return pwd_context.verify(plain_pass, hashed_pass)
    except Exception as e:
        print(f"Xatolik: {e}")
        return False


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        return db.query(User).filter(User.username == username).first()
    except JWTError:
        return None


@auth_router.get("/")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@auth_router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@auth_router.post("/login")
async def login(
        request: Request,
        db: Session = Depends(get_db),
        username: str = Form(...),
        password: str = Form(...),
):
    user = db.query(User).filter(User.username == username).first()
    for i in db.query(User).all():
        print(f"Username: {i.username}, Password Hash: {i.password}")
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "User not found"})

    if not await verify_pass(password, user.password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

    access_token = create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/tasks", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


@auth_router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="access_token")
    return response
