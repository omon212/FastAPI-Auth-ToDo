from fastapi import FastAPI, Form
from app.base.services import static, templates
from app.tasks import routers as tasks_routers
from starlette.middleware.sessions import SessionMiddleware
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from app.databace import *

app = FastAPI()

app.mount("/static", static, name="static")
app.add_middleware(SessionMiddleware, secret_key="52c5d29417b1fec270bcc67fb1ed8e941dd114f1f071ed2644e3be952ea45279", )
app.add_route("/tasks", tasks_routers.read_task, methods=["GET"])
app.add_route("/add_task", tasks_routers.add_task, methods=["POST"])
app.add_api_route("/del_task/{pk}", tasks_routers.del_task, methods=["POST"])


@app.get("/")
async def home(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    return RedirectResponse(url="/tasks", status_code=303)


@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


@app.post("/login")
async def login(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
):
    user = await auth_user(username, password)
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Invalid username or password.",
            },
        )
    request.session["user"] = user["username"]
    db[user["username"]]["tasks"] = []
    return RedirectResponse(url="/tasks", status_code=303)


@app.get("/logout")
async def logout(request: Request):
    print("")
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)
