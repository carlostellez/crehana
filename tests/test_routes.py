"""
Integration tests for TodoList REST API endpoints.

This module contains comprehensive tests for all REST API endpoints
including CRUD operations and error handling.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestTaskEndpoints:
    """
    Test class for task-related endpoints.
    """
    
    def test_health_check(self):
        """
        Test the health check endpoint.
        """
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy", "service": "TodoList API"}
    
    def test_get_all_tasks(self):
        """
        Test getting all tasks.
        """
        response = client.get("/tasks/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        # Should have initial sample tasks
        assert len(response.json()) >= 0
    
    def test_create_task(self):
        """
        Test creating a new task.
        """
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "completed": False
        }
        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 201
        
        created_task = response.json()
        assert created_task["title"] == task_data["title"]
        assert created_task["description"] == task_data["description"]
        assert created_task["completed"] == task_data["completed"]
        assert "id" in created_task
    
    def test_create_completed_task(self):
        """
        Test creating a completed task.
        """
        task_data = {
            "title": "Completed Task",
            "description": "This task is already completed",
            "completed": True
        }
        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 201
        
        created_task = response.json()
        assert created_task["completed"] is True
    
    def test_get_task_by_id(self):
        """
        Test getting a specific task by ID.
        """
        # First create a task
        task_data = {
            "title": "Get Test Task",
            "description": "Task for get test",
            "completed": False
        }
        create_response = client.post("/tasks/", json=task_data)
        created_task = create_response.json()
        task_id = created_task["id"]
        
        # Now get the task
        response = client.get(f"/tasks/{task_id}/")
        assert response.status_code == 200
        
        retrieved_task = response.json()
        assert retrieved_task["id"] == task_id
        assert retrieved_task["title"] == task_data["title"]
    
    def test_get_nonexistent_task(self):
        """
        Test getting a task that doesn't exist.
        """
        response = client.get("/tasks/99999/")
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"
    
    def test_update_task(self):
        """
        Test updating an existing task.
        """
        # First create a task
        task_data = {
            "title": "Update Test Task",
            "description": "Task for update test",
            "completed": False
        }
        create_response = client.post("/tasks/", json=task_data)
        created_task = create_response.json()
        task_id = created_task["id"]
        
        # Update the task
        update_data = {
            "title": "Updated Task Title",
            "description": "Updated description",
            "completed": True
        }
        response = client.put(f"/tasks/{task_id}/", json=update_data)
        assert response.status_code == 200
        
        updated_task = response.json()
        assert updated_task["title"] == update_data["title"]
        assert updated_task["description"] == update_data["description"]
        assert updated_task["completed"] == update_data["completed"]
    
    def test_update_partial_task(self):
        """
        Test updating only some fields of a task.
        """
        # First create a task
        task_data = {
            "title": "Partial Update Task",
            "description": "Original description",
            "completed": False
        }
        create_response = client.post("/tasks/", json=task_data)
        created_task = create_response.json()
        task_id = created_task["id"]
        
        # Update only the completed status
        update_data = {
            "completed": True
        }
        response = client.put(f"/tasks/{task_id}/", json=update_data)
        assert response.status_code == 200
        
        updated_task = response.json()
        assert updated_task["title"] == task_data["title"]  # Unchanged
        assert updated_task["description"] == task_data["description"]  # Unchanged
        assert updated_task["completed"] is True  # Changed
    
    def test_update_nonexistent_task(self):
        """
        Test updating a task that doesn't exist.
        """
        update_data = {
            "title": "Updated Title"
        }
        response = client.put("/tasks/99999/", json=update_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"
    
    def test_delete_task(self):
        """
        Test deleting a task.
        """
        # First create a task
        task_data = {
            "title": "Delete Test Task",
            "description": "Task for delete test",
            "completed": False
        }
        create_response = client.post("/tasks/", json=task_data)
        created_task = create_response.json()
        task_id = created_task["id"]
        
        # Delete the task
        response = client.delete(f"/tasks/{task_id}/")
        assert response.status_code == 204
        
        # Verify task is deleted
        get_response = client.get(f"/tasks/{task_id}/")
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_task(self):
        """
        Test deleting a task that doesn't exist.
        """
        response = client.delete("/tasks/99999/")
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

class TestTaskValidation:
    """
    Test class for task validation.
    """
    
    def test_create_task_missing_required_fields(self):
        """
        Test creating a task with missing required fields.
        """
        # Missing title
        task_data = {
            "description": "Task without title",
            "completed": False
        }
        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 422
        
        # Missing description
        task_data = {
            "title": "Task without description",
            "completed": False
        }
        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 422
    
    def test_create_task_invalid_completed_type(self):
        """
        Test creating a task with invalid completed field type.
        """
        task_data = {
            "title": "Invalid Completed Task",
            "description": "Task with invalid completed field",
            "completed": "not_a_boolean"
        }
        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 422 