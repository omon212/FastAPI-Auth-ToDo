from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")
static = StaticFiles(directory="static")


class BaseService:

    def __init__(self, request):
        self.request = request
