"""
REST API router for task operations.

This module contains all REST API endpoints for task management
with proper error handling and HTTP status codes.
"""

from typing import List

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.models.exceptions import TaskNotFoundException
from app.models.task import Task, TaskCreate, TaskUpdate
from app.services import task_service_instance

# Create router instance
router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"],
    responses={
        404: {"description": "Task not found"},
        400: {"description": "Bad request"},
    },
)

# Use the singleton task service instance
task_service = task_service_instance


@router.get(
    "/",
    response_model=List[Task],
    summary="Get all tasks",
    description="Retrieve all tasks from the TodoList.",
)
async def get_all_tasks() -> List[Task]:
    """
    Get all tasks from the TodoList.

    Returns:
        List[Task]: List of all tasks
    """
    return task_service.get_all_tasks()


@router.get(
    "/{task_id}",
    response_model=Task,
    summary="Get task by ID",
    description="Retrieve a specific task by its ID. Returns 404 if task is not found.",
    responses={
        200: {"description": "Task found and returned"},
        404: {"description": "Task not found"},
    },
)
async def get_task_by_id(task_id: int) -> Task:
    """
    Get a specific task by ID.

    Args:
        task_id: The ID of the task to retrieve

    Returns:
        Task: The task if found

    Raises:
        HTTPException: 404 if task is not found
    """
    return task_service.get_task_by_id_or_404(task_id)


@router.post(
    "/",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task in the TodoList.",
    responses={
        201: {"description": "Task created successfully"},
        400: {"description": "Invalid task data"},
    },
)
async def create_task(task_data: TaskCreate) -> Task:
    """
    Create a new task.

    Args:
        task_data: The task data to create

    Returns:
        Task: The created task
    """
    return task_service.create_task(task_data)


@router.put(
    "/{task_id}",
    response_model=Task,
    summary="Update task",
    description="Update an existing task by ID. Returns 404 if task is not found.",
    responses={
        200: {"description": "Task updated successfully"},
        404: {"description": "Task not found"},
        400: {"description": "Invalid task data"},
    },
)
async def update_task(task_id: int, task_data: TaskUpdate) -> Task:
    """
    Update an existing task.

    Args:
        task_id: The ID of the task to update
        task_data: The task data to update

    Returns:
        Task: The updated task

    Raises:
        HTTPException: 404 if task is not found
    """
    return task_service.update_task_or_404(task_id, task_data)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Delete a task by ID. Returns 404 if task is not found.",
    responses={
        204: {"description": "Task deleted successfully"},
        404: {"description": "Task not found"},
    },
)
async def delete_task(task_id: int) -> None:
    """
    Delete a task.

    Args:
        task_id: The ID of the task to delete

    Raises:
        HTTPException: 404 if task is not found
    """
    task_service.delete_task_or_404(task_id)
    return None
