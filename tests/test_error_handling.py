"""
Error handling tests for TodoList application.

This module contains tests that demonstrate different approaches
to error handling in both REST and GraphQL APIs.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import task_service_instance

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_tasks():
    """Clear all tasks before each test to ensure clean state."""
    task_service_instance.tasks_data.clear()


class TestRESTErrorHandling:
    """Test REST API error handling with proper HTTP status codes."""

    def test_get_nonexistent_task_returns_404(self):
        """Test that getting a non-existent task returns 404."""
        response = client.get("/api/v1/tasks/999")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Task with ID 999 not found" in data["detail"]

    def test_update_nonexistent_task_returns_404(self):
        """Test that updating a non-existent task returns 404."""
        update_data = {"title": "Updated Task", "completed": True}

        response = client.put("/api/v1/tasks/999", json=update_data)

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Task with ID 999 not found" in data["detail"]

    def test_delete_nonexistent_task_returns_404(self):
        """Test that deleting a non-existent task returns 404."""
        response = client.delete("/api/v1/tasks/999")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Task with ID 999 not found" in data["detail"]

    def test_successful_operations_after_creation(self):
        """Test that operations work correctly after creating a task."""
        # Create a task
        create_data = {
            "title": "Test Task",
            "description": "Test description",
            "completed": False,
        }

        response = client.post("/api/v1/tasks/", json=create_data)
        assert response.status_code == 201
        task = response.json()
        task_id = task["id"]

        # Get the task (should work)
        response = client.get(f"/api/v1/tasks/{task_id}")
        assert response.status_code == 200

        # Update the task (should work)
        update_data = {"completed": True}
        response = client.put(f"/api/v1/tasks/{task_id}", json=update_data)
        assert response.status_code == 200

        # Delete the task (should work)
        response = client.delete(f"/api/v1/tasks/{task_id}")
        assert response.status_code == 204

        # Try to get deleted task (should return 404)
        response = client.get(f"/api/v1/tasks/{task_id}")
        assert response.status_code == 404


class TestGraphQLErrorHandling:
    """Test GraphQL error handling approaches."""

    def test_graphql_task_returns_null_for_nonexistent(self):
        """Test that GraphQL task query returns null for non-existent task."""
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
        assert "errors" not in data or not data["errors"]

    def test_graphql_task_strict_returns_error_for_nonexistent(self):
        """Test that GraphQL taskStrict query returns error for non-existent task."""
        query = """
        query {
            taskStrict(taskId: 999) {
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
        assert "errors" in data
        assert len(data["errors"]) > 0

        error = data["errors"][0]
        assert "Task with ID 999 not found" in error["message"]
        assert "extensions" in error
        assert error["extensions"]["code"] == "TASK_NOT_FOUND"
        assert error["extensions"]["task_id"] == 999
        assert error["extensions"]["http_status"] == 404

    def test_graphql_update_task_returns_null_for_nonexistent(self):
        """Test that GraphQL updateTask mutation returns null for non-existent task."""
        mutation = """
        mutation {
            updateTask(taskId: 999, taskInput: {
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

        response = client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200

        data = response.json()
        assert "data" in data
        assert data["data"]["updateTask"] is None
        assert "errors" not in data or not data["errors"]

    def test_graphql_update_task_strict_returns_error_for_nonexistent(self):
        """Test that GraphQL updateTaskStrict mutation returns error for non-existent task."""
        mutation = """
        mutation {
            updateTaskStrict(taskId: 999, taskInput: {
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

        response = client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200

        data = response.json()
        assert "errors" in data
        assert len(data["errors"]) > 0

        error = data["errors"][0]
        assert "Task with ID 999 not found" in error["message"]
        assert "extensions" in error
        assert error["extensions"]["code"] == "TASK_NOT_FOUND"
        assert error["extensions"]["task_id"] == 999

    def test_graphql_delete_task_returns_false_for_nonexistent(self):
        """Test that GraphQL deleteTask mutation returns false for non-existent task."""
        mutation = """
        mutation {
            deleteTask(taskId: 999)
        }
        """

        response = client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200

        data = response.json()
        assert "data" in data
        assert data["data"]["deleteTask"] is False
        assert "errors" not in data or not data["errors"]

    def test_graphql_delete_task_strict_returns_error_for_nonexistent(self):
        """Test that GraphQL deleteTaskStrict mutation returns error for non-existent task."""
        mutation = """
        mutation {
            deleteTaskStrict(taskId: 999)
        }
        """

        response = client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200

        data = response.json()
        assert "errors" in data
        assert len(data["errors"]) > 0

        error = data["errors"][0]
        assert "Task with ID 999 not found" in error["message"]
        assert "extensions" in error
        assert error["extensions"]["code"] == "TASK_NOT_FOUND"

    def test_graphql_successful_operations_with_both_approaches(self):
        """Test that both GraphQL approaches work correctly with existing tasks."""
        # Create a task first
        mutation_create = """
        mutation {
            createTask(taskInput: {
                title: "Test Task"
                description: "Test description"
                completed: false
            }) {
                id
                title
                description
                completed
            }
        }
        """

        response = client.post("/graphql", json={"query": mutation_create})
        assert response.status_code == 200

        data = response.json()
        task_id = data["data"]["createTask"]["id"]

        # Test regular task query
        query_regular = f"""
        query {{
            task(taskId: {task_id}) {{
                id
                title
                completed
            }}
        }}
        """

        response = client.post("/graphql", json={"query": query_regular})
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["task"] is not None
        assert data["data"]["task"]["id"] == task_id

        # Test strict task query
        query_strict = f"""
        query {{
            taskStrict(taskId: {task_id}) {{
                id
                title
                completed
            }}
        }}
        """

        response = client.post("/graphql", json={"query": query_strict})
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["taskStrict"] is not None
        assert data["data"]["taskStrict"]["id"] == task_id
        assert "errors" not in data or not data["errors"]


class TestErrorHandlingComparison:
    """Test class to demonstrate the differences between REST and GraphQL error handling."""

    def test_error_response_format_comparison(self):
        """Compare error response formats between REST and GraphQL."""
        # REST API error response
        rest_response = client.get("/api/v1/tasks/999")
        assert rest_response.status_code == 404
        rest_data = rest_response.json()

        # GraphQL error response (strict mode)
        graphql_query = """
        query {
            taskStrict(taskId: 999) {
                id
                title
            }
        }
        """

        graphql_response = client.post("/graphql", json={"query": graphql_query})
        assert graphql_response.status_code == 200  # GraphQL always returns 200
        graphql_data = graphql_response.json()

        # Verify REST error format
        assert "detail" in rest_data
        assert "Task with ID 999 not found" in rest_data["detail"]

        # Verify GraphQL error format
        assert "errors" in graphql_data
        assert "data" in graphql_data
        error = graphql_data["errors"][0]
        assert "message" in error
        assert "extensions" in error
        assert error["extensions"]["code"] == "TASK_NOT_FOUND"
        assert error["extensions"]["http_status"] == 404

        print("\n=== REST Error Response ===")
        print(f"Status Code: {rest_response.status_code}")
        print(f"Response: {rest_data}")

        print("\n=== GraphQL Error Response ===")
        print(f"Status Code: {graphql_response.status_code}")
        print(f"Response: {graphql_data}")
