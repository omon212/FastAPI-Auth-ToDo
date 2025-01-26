from app.base.services import BaseService, templates
from app.databace import db
from fastapi.responses import RedirectResponse


class TaskService(BaseService):
    async def read_task(self, request):
        user = request.session.get("user")
        if not user:
            return RedirectResponse(url="/login", status_code=303)
        tasks = db.get(user).get("tasks")
        if not tasks:
            tasks = []
        return templates.TemplateResponse(
            "todos.html",
            {
                "request": self.request,
                "tasks": tasks
            }
        )

    async def add_task(self, request):
        user = request.session.get("user")
        if not user:
            return RedirectResponse(url="/login", status_code=303)
        task = await self.request.form()
        new_id = len(db[user]["tasks"]) + 1
        new_task = {
            "id": new_id,
            "title": task["title"],
            "time": task["time"],
            "description": task["description"],
            "status": "Bajarilmagan"
        }
        db[user]["tasks"].append(new_task)
        return RedirectResponse("/tasks", status_code=303)

    async def del_task(self, request, pk: int):
        user = request.session.get("user")
        if not user:
            return RedirectResponse(url="/login", status_code=303)
        tasks = db.get(user, {}).get("tasks", [])
        db[user]["tasks"] = [task for task in tasks if task.get("id") != pk]
        return RedirectResponse(url="/tasks", status_code=303)
