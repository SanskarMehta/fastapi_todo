from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class TasksCreate(BaseModel):
    title: str = Field(..., title='Title', max_length=55, min_length=1)
    description: str = Field(..., title='Title', max_length=755, min_length=1)
    status: Optional[bool] = False


class TasksUpdate(BaseModel):
    title: Optional[str] = Field(title='Title', max_length=55, min_length=1)
    description: Optional[str] = Field(title='Title', max_length=755, min_length=1)
    status: Optional[bool] = None


class TasksOut(BaseModel):
    todo_id: UUID
    status: bool
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
