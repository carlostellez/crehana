"""
Routers package for TodoList application.

This package contains all REST API routers and endpoints for the TodoList API.
"""

from .tasks import router as tasks_router

__all__ = ["tasks_router"]
