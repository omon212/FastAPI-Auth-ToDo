from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.databace import get_db, User, Tasks
from app.base.services import templates
from app.auth import get_current_user

tasks_router = APIRouter()


@tasks_router.get("/tasks")
async def read_tasks(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    tasks = db.query(Tasks).filter(Tasks.user_id == current_user.id).all()
    return templates.TemplateResponse("todos.html", {"request": request, "tasks": tasks})


@tasks_router.post("/add_task")
async def add_task(
        title: str = Form(...),
        time: str = Form(...),
        description: str = Form(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    new_task = Tasks(title=title, time=time, description=description, status="Bajarilmagan", user_id=current_user.id)
    db.add(new_task)
    db.commit()
    return RedirectResponse(url="/tasks", status_code=303)


@tasks_router.post("/del_task/{pk}")
async def delete_task(pk: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    task = db.query(Tasks).filter(Tasks.id == pk, Tasks.user_id == current_user.id).first()
    if not task:
        return RedirectResponse(url="/tasks", status_code=303)
    db.delete(task)
    db.commit()
    return RedirectResponse(url="/tasks", status_code=303)
