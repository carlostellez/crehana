"""
Task model and schemas for TodoList application.

This module defines the Task data model, enums, and related Pydantic schemas
for managing todo items.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskStatus(str, Enum):
    """
    Task status enumeration.
    """

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """
    Task priority enumeration.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskBase(BaseModel):
    """
    Base Task schema with common fields.
    """

    title: str
    description: str
    completed: bool = False


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    """

    pass


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Task(TaskBase):
    """
    Complete Task schema with all fields.
    """

    id: int

    model_config = ConfigDict(from_attributes=True)
