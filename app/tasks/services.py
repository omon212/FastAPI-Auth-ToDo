from app.base.services import BaseService, templates
from app.databace import db
from fastapi.responses import RedirectResponse


class TaskService(BaseService):

    async def read_task(self, request):
        user = request.session.get("user")
        if not user:
            return RedirectResponse(url="/login", status_code=303)
        tasks = db["tasks"]
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
        new_id = len(db["tasks"]) + 1
        new_task = {
            "id": new_id,
            "title": task["title"],
            "time": task["time"],
            "description": task["description"],
            "status": "Bajarilmagan"
        }
        db["tasks"].append(new_task)
        return RedirectResponse("/tasks", status_code=303)

    async def del_task(self,request ,pk: int):
        user = request.session.get("user")
        if not user:
            return RedirectResponse(url="/login", status_code=303)
        user = request.session.get("user")
        db['tasks'] = [task for task in db['tasks'] if task['id'] != pk]
        return RedirectResponse(url="/tasks", status_code=303)
