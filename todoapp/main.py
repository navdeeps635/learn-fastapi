from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from fastapi import FastAPI, Depends, HTTPException, Path
from starlette import status
import models
from database import engine
from routers import auth, todos, admin


app = FastAPI(title='FastAPI Todo App')
models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)