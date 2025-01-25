from fastapi.requests import Request
from app.tasks import services as svc


async def read_task(request: Request):
    return await svc.TaskService(request).read_task(request)


async def add_task(request: Request):
    return await svc.TaskService(request).add_task(request)


async def del_task(request: Request, pk: int):
    return await svc.TaskService(request).del_task(request, pk)
