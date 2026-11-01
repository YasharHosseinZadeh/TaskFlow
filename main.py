from fastapi import FastAPI
from routers import users,projects

app = FastAPI(title="TaskFlow API")

app.include_router(users.router)
app.include_router(projects.router)