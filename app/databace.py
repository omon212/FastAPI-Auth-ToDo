from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def verify_pass(plain_pass: str, hashed_pass: str):
    return pwd_context.verify(plain_pass, hashed_pass)

async def auth_user(username: str, password: str):
    user = db.get(username)
    if not user:
        return None
    if not await verify_pass(password, user["password"]):
        return None
    return user

db = {
    "omon212": {
        "username": "omon212",
        "password": pwd_context.hash("omonullo66"),
    }
}
