"""
Custom exceptions for the TodoList application.

This module defines custom exception classes used throughout the application
for proper error handling and HTTP status code mapping.
"""

from fastapi import HTTPException, status


class TaskNotFoundException(HTTPException):
    """
    Exception raised when a task is not found by ID.

    This exception automatically maps to HTTP 404 status code.
    """

    def __init__(self, task_id: int):
        """
        Initialize the TaskNotFoundException.

        Args:
            task_id: The ID of the task that was not found
        """
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )


class TaskValidationException(HTTPException):
    """
    Exception raised when task validation fails.

    This exception automatically maps to HTTP 400 status code.
    """

    def __init__(self, message: str):
        """
        Initialize the TaskValidationException.

        Args:
            message: The validation error message
        """
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        ) 