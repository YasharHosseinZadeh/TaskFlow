from fastapi import FastAPI
from routers import users

app = FastAPI(title="TaskFlow API")

app.include_router(users.router)