from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import (
    init_db,
    get_all_tasks,
    add_task,
    update_task,
    delete_task,
    get_task_by_id,
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static") # Static files-CSS
templates = Jinja2Templates(directory="templates") # HTML templates

# Initialize DB on startup
@app.on_event("startup")
async def startup():
    await init_db()

# Home page: show all tasks
@app.get("/", response_class=HTMLResponse)
async def read_tasks(request: Request):
    tasks = await get_all_tasks()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

# Add new task
@app.post("/add")
async def create_task(task_name: str = Form(...), description: str = Form(""), person: str = Form(""), status: str = Form("pending")):
    await add_task(task_name, description, person, status)
    return RedirectResponse("/", status_code=303)

# Delete a task
@app.post("/delete/{task_id}")
async def remove_task(task_id: int):
    await delete_task(task_id)
    return RedirectResponse("/", status_code=303)

# Edit form page (GET)
@app.get("/edit/{task_id}", response_class=HTMLResponse)
async def edit_task_page(request: Request, task_id: int):
    task = await get_task_by_id(task_id)
    if not task:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("edit.html", {"request": request, "task": task})

# Update task (POST)
@app.post("/update/{task_id}")
async def apply_task_update(task_id: int, task_name: str = Form(...), description: str = Form(""), person: str = Form(""), status: str = Form("pending")):
    await update_task(task_id, task_name, description, person, status)
    return RedirectResponse("/", status_code=303)
