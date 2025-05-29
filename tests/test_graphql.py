"""
GraphQL tests for the TodoList application.

This module contains integration tests for all GraphQL operations
using Strawberry GraphQL with FastAPI.
"""

import pytest
from fastapi.testclient import TestClient

from app.graphql.resolvers import task_service
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_tasks():
    """Clear all tasks before each test to ensure clean state."""
    # Access the global task service instance used by resolvers
    task_service.tasks_data.clear()


class TestGraphQLQueries:
    """Test GraphQL query operations."""

    def test_get_all_tasks_empty(self):
        """Test getting all tasks when list is empty."""
        query = """
        query {
            tasks {
                id
                title
                description
                completed
            }
        }
        """

        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200

        data = response.json()
        assert "data" in data
        assert "tasks" in data["data"]
        assert data["data"]["tasks"] == []

    def test_get_task_not_found(self):
        """Test getting a task that doesn't exist."""
        query = """
        query {
            task(taskId: 999) {
                id
                title
                description
                completed
            }
        }
        """

        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200

        data = response.json()
        assert "data" in data
        assert data["data"]["task"] is None


class TestGraphQLMutations:
    """Test GraphQL mutation operations."""

    def test_create_task(self):
        """Test creating a new task."""
        mutation = """
        mutation {
            createTask(taskInput: {
                title: "Test Task"
                description: "This is a test task"
                completed: false
            }) {
                id
                title
                description
                completed
            }
        }
        """

        response = client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200

        data = response.json()
        assert "data" in data
        assert "createTask" in data["data"]

        task = data["data"]["createTask"]
        assert task["id"] == 1
        assert task["title"] == "Test Task"
        assert task["description"] == "This is a test task"
        assert task["completed"] is False

    def test_get_task_after_creation(self):
        """Test getting a task after it's been created."""
        # First create a task
        mutation = """
        mutation {
            createTask(taskInput: {
                title: "Another Task"
                description: "Another test task"
                completed: true
            }) {
                id
            }
        }
        """

        response = client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200

        # Then get the task
        query = """
        query {
            task(taskId: 1) {
                id
                title
                description
                completed
            }
        }
        """

        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200

        data = response.json()
        assert "data" in data
        assert "task" in data["data"]

        task = data["data"]["task"]
        assert task["id"] == 1
        assert task["title"] == "Another Task"
        assert task["description"] == "Another test task"
        assert task["completed"] is True

    def test_get_all_tasks_with_data(self):
        """Test getting all tasks when there are tasks in the list."""
        # First create two tasks
        mutation1 = """
        mutation {
            createTask(taskInput: {
                title: "First Task"
                description: "First test task"
                completed: false
            }) {
                id
            }
        }
        """

        mutation2 = """
        mutation {
            createTask(taskInput: {
                title: "Second Task"
                description: "Second test task"
                completed: true
            }) {
                id
            }
        }
        """

        client.post("/graphql", json={"query": mutation1})
        client.post("/graphql", json={"query": mutation2})

        # Now get all tasks
        query = """
        query {
            tasks {
                id
                title
                description
                completed
            }
        }
        """

        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200

        data = response.json()
        assert "data" in data
        assert "tasks" in data["data"]

        tasks = data["data"]["tasks"]
        assert len(tasks) == 2

        # Check first task
        assert tasks[0]["id"] == 1
        assert tasks[0]["title"] == "First Task"

        # Check second task
        assert tasks[1]["id"] == 2
        assert tasks[1]["title"] == "Second Task"

    def test_update_task(self):
        """Test updating an existing task."""
        # First create a task
        mutation_create = """
        mutation {
            createTask(taskInput: {
                title: "Original Task"
                description: "Original description"
                completed: false
            }) {
                id
            }
        }
        """

        client.post("/graphql", json={"query": mutation_create})

        # Then update it
        mutation_update = """
        mutation {
            updateTask(taskId: 1, taskInput: {
                title: "Updated Task"
                completed: true
            }) {
                id
                title
                description
                completed
            }
        }
        """

        response = client.post("/graphql", json={"query": mutation_update})
        assert response.status_code == 200

        data = response.json()
        assert "data" in data
        assert "updateTask" in data["data"]

        task = data["data"]["updateTask"]
        assert task["id"] == 1
        assert task["title"] == "Updated Task"
        assert task["description"] == "Original description"  # Should remain unchanged
        assert task["completed"] is True

    def test_update_task_not_found(self):
        """Test updating a task that doesn't exist."""
        mutation = """
        mutation {
            updateTask(taskId: 999, taskInput: {
                title: "Non-existent Task"
            }) {
                id
                title
                description
                completed
            }
        }
        """

        response = client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200

        data = response.json()
        assert "data" in data
        assert data["data"]["updateTask"] is None

    def test_delete_task(self):
        """Test deleting an existing task."""
        # First create a task
        mutation_create = """
        mutation {
            createTask(taskInput: {
                title: "Task to Delete"
                description: "This task will be deleted"
                completed: false
            }) {
                id
            }
        }
        """

        client.post("/graphql", json={"query": mutation_create})

        # Then delete it
        mutation_delete = """
        mutation {
            deleteTask(taskId: 1)
        }
        """

        response = client.post("/graphql", json={"query": mutation_delete})
        assert response.status_code == 200

        data = response.json()
        assert "data" in data
        assert "deleteTask" in data["data"]
        assert data["data"]["deleteTask"] is True

        # Verify task is deleted by trying to get it
        query = """
        query {
            task(taskId: 1) {
                id
            }
        }
        """

        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200

        data = response.json()
        assert data["data"]["task"] is None

    def test_delete_task_not_found(self):
        """Test deleting a task that doesn't exist."""
        mutation = """
        mutation {
            deleteTask(taskId: 999)
        }
        """

        response = client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200

        data = response.json()
        assert "data" in data
        assert "deleteTask" in data["data"]
        assert data["data"]["deleteTask"] is False


class TestHealthCheck:
    """Test health check endpoint."""

    def test_health_check(self):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "TodoList GraphQL API"
