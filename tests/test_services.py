"""
Unit tests for TodoList service classes.

This module contains unit tests for the business logic layer services
including TaskService.
"""

import pytest
from app.services.task_service import TaskService
from app.models.task import TaskCreate, TaskUpdate

class TestTaskService:
    """
    Unit tests for TaskService class.
    """
    
    def setup_method(self):
        """
        Set up test fixtures before each test method.
        """
        self.task_service = TaskService()
    
    def test_get_all_tasks(self):
        """
        Test getting all tasks.
        """
        tasks = self.task_service.get_all_tasks()
        assert len(tasks) >= 3  # Should have initial sample tasks
        assert all(hasattr(task, 'id') for task in tasks)
        assert all(hasattr(task, 'title') for task in tasks)
        assert all(hasattr(task, 'description') for task in tasks)
        assert all(hasattr(task, 'completed') for task in tasks)
    
    def test_get_task_by_id_existing(self):
        """
        Test getting an existing task by ID.
        """
        task = self.task_service.get_task_by_id(1)
        assert task is not None
        assert task.id == 1
        assert task.title == "Complete project documentation"
        assert task.completed is False
    
    def test_get_task_by_id_nonexistent(self):
        """
        Test getting a non-existent task by ID.
        """
        task = self.task_service.get_task_by_id(99999)
        assert task is None
    
    def test_create_task_success(self):
        """
        Test creating a new task successfully.
        """
        task_data = TaskCreate(
            title="Test Task",
            description="Test description",
            completed=False
        )
        created_task = self.task_service.create_task(task_data)
        
        assert created_task.title == "Test Task"
        assert created_task.description == "Test description"
        assert created_task.completed is False
        assert isinstance(created_task.id, int)
    
    def test_create_completed_task(self):
        """
        Test creating a task that is already completed.
        """
        task_data = TaskCreate(
            title="Completed Task",
            description="This task is already done",
            completed=True
        )
        created_task = self.task_service.create_task(task_data)
        
        assert created_task.title == "Completed Task"
        assert created_task.completed is True
    
    def test_update_task_success(self):
        """
        Test updating a task successfully.
        """
        update_data = TaskUpdate(
            title="Updated Task",
            completed=True
        )
        updated_task = self.task_service.update_task(1, update_data)
        
        assert updated_task is not None
        assert updated_task.title == "Updated Task"
        assert updated_task.completed is True
    
    def test_update_task_partial(self):
        """
        Test updating only some fields of a task.
        """
        # Get original task
        original_task = self.task_service.get_task_by_id(1)
        
        # Update only completed status
        update_data = TaskUpdate(completed=True)
        updated_task = self.task_service.update_task(1, update_data)
        
        assert updated_task is not None
        assert updated_task.title == original_task.title  # Unchanged
        assert updated_task.description == original_task.description  # Unchanged
        assert updated_task.completed is True  # Changed
    
    def test_update_task_nonexistent(self):
        """
        Test updating a non-existent task.
        """
        update_data = TaskUpdate(title="Updated Title")
        updated_task = self.task_service.update_task(99999, update_data)
        
        assert updated_task is None
    
    def test_delete_task_success(self):
        """
        Test deleting a task successfully.
        """
        # First create a task to delete
        task_data = TaskCreate(
            title="Delete Me",
            description="Task to delete",
            completed=False
        )
        created_task = self.task_service.create_task(task_data)
        
        # Delete the task
        success = self.task_service.delete_task(created_task.id)
        assert success is True
        
        # Verify task is deleted
        deleted_task = self.task_service.get_task_by_id(created_task.id)
        assert deleted_task is None
    
    def test_delete_task_nonexistent(self):
        """
        Test deleting a non-existent task.
        """
        success = self.task_service.delete_task(99999)
        assert success is False
    
    def test_task_completion_workflow(self):
        """
        Test the complete workflow of creating and completing a task.
        """
        # Create a new task
        task_data = TaskCreate(
            title="Workflow Test",
            description="Test the complete workflow",
            completed=False
        )
        created_task = self.task_service.create_task(task_data)
        
        assert created_task.completed is False
        
        # Mark as completed
        update_data = TaskUpdate(completed=True)
        completed_task = self.task_service.update_task(created_task.id, update_data)
        
        assert completed_task is not None
        assert completed_task.completed is True
        assert completed_task.title == "Workflow Test"
    
    def test_multiple_tasks_creation(self):
        """
        Test creating multiple tasks and verifying they all exist.
        """
        initial_count = len(self.task_service.get_all_tasks())
        
        # Create multiple tasks
        for i in range(3):
            task_data = TaskCreate(
                title=f"Task {i+1}",
                description=f"Description for task {i+1}",
                completed=False
            )
            self.task_service.create_task(task_data)
        
        final_count = len(self.task_service.get_all_tasks())
        assert final_count == initial_count + 3 