from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
import models
from database import sessionLocal
from .auth import get_current_user


router = APIRouter(prefix="/admin", tags=["Admin"])

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed.")
    todos = db.query(models.Todo).all()
    return todos

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed.")
    todo_model = db.query(models.Todo).filter(models.Todo.id == todo_id).filter(models.Todo.owner_id==user.get("id")).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    db.delete(todo_model)
    db.commit()