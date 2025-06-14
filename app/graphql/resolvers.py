"""
GraphQL resolvers for the TodoList application.

This module contains all GraphQL queries and mutations
for task operations using Strawberry GraphQL.
"""

from typing import List, Optional

import strawberry
from strawberry.exceptions import GraphQLError

from app.graphql.types import Task, TaskInput, TaskUpdateInput
from app.models.exceptions import TaskNotFoundException
from app.models.task import TaskCreate, TaskUpdate
from app.services import task_service_instance

# Use the singleton task service instance
task_service = task_service_instance


def convert_to_graphql_task(pydantic_task) -> Task:
    """
    Convert a Pydantic Task to GraphQL Task.

    Args:
        pydantic_task: The Pydantic task model

    Returns:
        Task: The GraphQL task type
    """
    return Task(
        id=pydantic_task.id,
        title=pydantic_task.title,
        description=pydantic_task.description,
        completed=pydantic_task.completed,
    )


@strawberry.type
class Query:
    """
    GraphQL Query type containing all read operations.
    """

    @strawberry.field
    def tasks(self) -> List[Task]:
        """
        Get all tasks from the TodoList.

        Returns:
            List[Task]: List of all tasks
        """
        pydantic_tasks = task_service.get_all_tasks()
        return [
            Task(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
            )
            for task in pydantic_tasks
        ]

    @strawberry.field
    def task(self, task_id: int) -> Optional[Task]:
        """
        Get a specific task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Optional[Task]: The task if found, None otherwise
        """
        pydantic_task = task_service.get_task_by_id(task_id)
        if not pydantic_task:
            return None

        return Task(
            id=pydantic_task.id,
            title=pydantic_task.title,
            description=pydantic_task.description,
            completed=pydantic_task.completed,
        )

    @strawberry.field
    def task_strict(self, task_id: int) -> Task:
        """
        Get a specific task by ID with strict error handling.

        This method raises a GraphQL error if the task is not found,
        providing explicit error information in the response.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Task: The task if found

        Raises:
            GraphQLError: If the task is not found
        """
        try:
            return convert_to_graphql_task(task_service.get_task_by_id_or_404(task_id))
        except TaskNotFoundException as e:
            raise GraphQLError(
                message=str(e.detail),
                extensions={
                    "code": "TASK_NOT_FOUND",
                    "task_id": task_id,
                    "http_status": e.status_code,
                },
            ) from e


@strawberry.type
class Mutation:
    """
    GraphQL Mutation type containing all write operations.
    """

    @strawberry.mutation
    def create_task(self, task_input: TaskInput) -> Task:
        """
        Create a new task.

        Args:
            task_input: The task data to create

        Returns:
            Task: The created task
        """
        task_create = TaskCreate(
            title=task_input.title,
            description=task_input.description,
            completed=task_input.completed,
        )

        pydantic_task = task_service.create_task(task_create)

        return Task(
            id=pydantic_task.id,
            title=pydantic_task.title,
            description=pydantic_task.description,
            completed=pydantic_task.completed,
        )

    @strawberry.mutation
    def update_task(self, task_id: int, task_input: TaskUpdateInput) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: The ID of the task to update
            task_input: The task data to update

        Returns:
            Optional[Task]: The updated task if found, None otherwise
        """
        # Create TaskUpdate object with only non-None values
        update_data = {}
        if task_input.title is not None:
            update_data["title"] = task_input.title
        if task_input.description is not None:
            update_data["description"] = task_input.description
        if task_input.completed is not None:
            update_data["completed"] = task_input.completed

        task_update = TaskUpdate(**update_data)
        pydantic_task = task_service.update_task(task_id, task_update)

        if not pydantic_task:
            return None

        return Task(
            id=pydantic_task.id,
            title=pydantic_task.title,
            description=pydantic_task.description,
            completed=pydantic_task.completed,
        )

    @strawberry.mutation
    def update_task_strict(self, task_id: int, task_input: TaskUpdateInput) -> Task:
        """
        Update an existing task with strict error handling.

        This method raises a GraphQL error if the task is not found,
        providing explicit error information in the response.

        Args:
            task_id: The ID of the task to update
            task_input: The task data to update

        Returns:
            Task: The updated task

        Raises:
            GraphQLError: If the task is not found
        """
        try:
            # Create TaskUpdate object with only non-None values
            update_data = {}
            if task_input.title is not None:
                update_data["title"] = task_input.title
            if task_input.description is not None:
                update_data["description"] = task_input.description
            if task_input.completed is not None:
                update_data["completed"] = task_input.completed

            task_update = TaskUpdate(**update_data)
            pydantic_task = task_service.update_task_or_404(task_id, task_update)

            return Task(
                id=pydantic_task.id,
                title=pydantic_task.title,
                description=pydantic_task.description,
                completed=pydantic_task.completed,
            )
        except TaskNotFoundException as e:
            raise GraphQLError(
                message=str(e.detail),
                extensions={
                    "code": "TASK_NOT_FOUND",
                    "task_id": task_id,
                    "http_status": e.status_code,
                },
            ) from e

    @strawberry.mutation
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task.

        Args:
            task_id: The ID of the task to delete

        Returns:
            bool: True if the task was deleted, False if not found
        """
        return task_service.delete_task(task_id)

    @strawberry.mutation
    def delete_task_strict(self, task_id: int) -> bool:
        """
        Delete a task with strict error handling.

        This method raises a GraphQL error if the task is not found,
        providing explicit error information in the response.

        Args:
            task_id: The ID of the task to delete

        Returns:
            bool: True if the task was deleted

        Raises:
            GraphQLError: If the task is not found
        """
        try:
            return task_service.delete_task_or_404(task_id)
        except TaskNotFoundException as e:
            raise GraphQLError(
                message=str(e.detail),
                extensions={
                    "code": "TASK_NOT_FOUND",
                    "task_id": task_id,
                    "http_status": e.status_code,
                },
            ) from e
