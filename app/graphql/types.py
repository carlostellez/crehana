"""
GraphQL types for the TodoList application.

This module defines all GraphQL types using Strawberry GraphQL
for the Task entity and related input/output types.
"""

from typing import Optional

import strawberry


@strawberry.type
class Task:
    """
    GraphQL type representing a task in the TodoList.

    Attributes:
        id: Unique identifier for the task
        title: Title of the task
        description: Detailed description of the task
        completed: Boolean indicating if the task is completed
    """

    id: int
    title: str
    description: str
    completed: bool


@strawberry.input
class TaskInput:
    """
    GraphQL input type for creating a new task.

    Attributes:
        title: Title of the task
        description: Detailed description of the task
        completed: Boolean indicating if the task is completed (defaults to False)
    """

    title: str
    description: str
    completed: bool = False


@strawberry.input
class TaskUpdateInput:
    """
    GraphQL input type for updating an existing task.

    All fields are optional to allow partial updates.

    Attributes:
        title: Optional new title for the task
        description: Optional new description for the task
        completed: Optional new completion status for the task
    """

    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
