"""
Task service for TodoList application.

This module contains the TaskService class that handles all task-related
business logic and operations.
"""

from datetime import datetime
from typing import List, Optional

from app.models.exceptions import TaskNotFoundException
from app.models.task import Task, TaskCreate, TaskUpdate


class TaskService:
    """
    Service class for handling task operations.

    This class contains all business logic related to task management
    including creation, retrieval, updating, and validation.
    """

    def __init__(self):
        """
        Initialize the TaskService with empty data.
        """
        # In-memory storage for demonstration - starts empty
        self.tasks_data = []

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks.

        Returns:
            List[Task]: List of all tasks
        """
        return [
            Task(
                id=task["id"],
                title=task["title"],
                description=task["description"],
                completed=task["completed"],
            )
            for task in self.tasks_data
        ]

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a specific task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Optional[Task]: The task if found, None otherwise
        """
        task_dict = next(
            (task for task in self.tasks_data if task["id"] == task_id), None
        )
        if task_dict:
            return Task(
                id=task_dict["id"],
                title=task_dict["title"],
                description=task_dict["description"],
                completed=task_dict["completed"],
            )
        return None

    def get_task_by_id_or_404(self, task_id: int) -> Task:
        """
        Retrieve a specific task by ID or raise 404 exception.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Task: The task if found

        Raises:
            TaskNotFoundException: If the task is not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            raise TaskNotFoundException(task_id)
        return task

    def create_task(self, task_data: TaskCreate) -> Task:
        """
        Create a new task.

        Args:
            task_data: The task data to create

        Returns:
            Task: The created task
        """
        new_id = max([task["id"] for task in self.tasks_data], default=0) + 1
        new_task = {
            "id": new_id,
            "title": task_data.title,
            "description": task_data.description,
            "completed": task_data.completed,
        }
        self.tasks_data.append(new_task)

        return Task(
            id=new_task["id"],
            title=new_task["title"],
            description=new_task["description"],
            completed=new_task["completed"],
        )

    def update_task(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: The ID of the task to update
            task_data: The task data to update

        Returns:
            Optional[Task]: The updated task if found, None otherwise
        """
        task_dict = next(
            (task for task in self.tasks_data if task["id"] == task_id), None
        )
        if not task_dict:
            return None

        # Update fields if provided
        if task_data.title is not None:
            task_dict["title"] = task_data.title
        if task_data.description is not None:
            task_dict["description"] = task_data.description
        if task_data.completed is not None:
            task_dict["completed"] = task_data.completed

        return Task(
            id=task_dict["id"],
            title=task_dict["title"],
            description=task_dict["description"],
            completed=task_dict["completed"],
        )

    def update_task_or_404(self, task_id: int, task_data: TaskUpdate) -> Task:
        """
        Update an existing task or raise 404 exception.

        Args:
            task_id: The ID of the task to update
            task_data: The task data to update

        Returns:
            Task: The updated task

        Raises:
            TaskNotFoundException: If the task is not found
        """
        task = self.update_task(task_id, task_data)
        if not task:
            raise TaskNotFoundException(task_id)
        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task.

        Args:
            task_id: The ID of the task to delete

        Returns:
            bool: True if task was deleted, False if not found
        """
        task_index = next(
            (i for i, task in enumerate(self.tasks_data) if task["id"] == task_id), None
        )
        if task_index is not None:
            self.tasks_data.pop(task_index)
            return True
        return False

    def delete_task_or_404(self, task_id: int) -> bool:
        """
        Delete a task or raise 404 exception.

        Args:
            task_id: The ID of the task to delete

        Returns:
            bool: True if task was deleted

        Raises:
            TaskNotFoundException: If the task is not found
        """
        success = self.delete_task(task_id)
        if not success:
            raise TaskNotFoundException(task_id)
        return success
