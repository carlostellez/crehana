"""
Services package for TodoList application.

This package contains all business logic services and provides
singleton instances for shared state across the application.
"""

from .task_service import TaskService

# Create a singleton instance of TaskService to share state across the application
task_service_instance = TaskService()

__all__ = ["TaskService", "task_service_instance"]
