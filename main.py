from fastapi import FastAPI

from routers import projects, tasks, users

app = FastAPI(title="TaskFlow API")

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)