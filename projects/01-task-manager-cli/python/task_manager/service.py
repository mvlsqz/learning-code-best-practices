"""
Task Service - Demonstrates SRP and DIP

SRP: This class is responsible ONLY for task business logic (CRUD operations).
     It doesn't handle storage, formatting, or CLI interaction.
DIP: Depends on IStorage abstraction, not concrete implementation.
"""
from typing import List, Optional, Callable
from task_manager.task import Task
from task_manager.storage import IStorage


class TaskService:
    """
    Manages task business logic.
    
    SRP: Single responsibility - coordinate task operations.
    DIP: Depends on IStorage interface, not concrete storage class.
    """
    
    def __init__(self, storage: IStorage):
        """
        Initialize with storage dependency.
        
        DIP: We depend on the IStorage abstraction.
        The actual storage type is injected (dependency injection).
        """
        self.storage = storage
    
    def add_task(self, task: Task) -> None:
        """Add a new task."""
        tasks = self.storage.load()
        tasks.append(task)
        self.storage.save(tasks)
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks."""
        return self.storage.load()
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Get a specific task by ID."""
        tasks = self.storage.load()
        for task in tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_task_by_index(self, index: int) -> Optional[Task]:
        """Get a task by its list index."""
        tasks = self.storage.load()
        if 0 <= index < len(tasks):
            return tasks[index]
        return None
    
    def update_task(self, task_id: str, **updates) -> bool:
        """
        Update a task's attributes.
        
        Args:
            task_id: The task's unique identifier
            **updates: Keyword arguments for fields to update
            
        Returns:
            True if task was updated, False if not found
        """
        tasks = self.storage.load()
        for task in tasks:
            if task.id == task_id:
                for key, value in updates.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                self.storage.save(tasks)
                return True
        return False
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task by ID.
        
        Returns:
            True if task was deleted, False if not found
        """
        tasks = self.storage.load()
        original_length = len(tasks)
        tasks = [t for t in tasks if t.id != task_id]
        
        if len(tasks) < original_length:
            self.storage.save(tasks)
            return True
        return False
    
    def delete_task_by_index(self, index: int) -> bool:
        """
        Delete a task by its list index.
        
        Returns:
            True if task was deleted, False if index invalid
        """
        tasks = self.storage.load()
        if 0 <= index < len(tasks):
            tasks.pop(index)
            self.storage.save(tasks)
            return True
        return False
    
    def complete_task(self, task_id: str) -> bool:
        """Mark a task as completed."""
        return self.update_task(task_id, completed=True)
    
    def complete_task_by_index(self, index: int) -> bool:
        """Mark a task as completed by index."""
        task = self.get_task_by_index(index)
        if task:
            return self.complete_task(task.id)
        return False
    
    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Search tasks by keyword in title or description.
        
        Args:
            keyword: Search term (case-insensitive)
            
        Returns:
            List of matching tasks
        """
        tasks = self.storage.load()
        keyword_lower = keyword.lower()
        return [
            task for task in tasks
            if keyword_lower in task.title.lower()
            or keyword_lower in task.description.lower()
        ]
    
    def filter_tasks(self, filter_func: Callable[[Task], bool]) -> List[Task]:
        """
        Filter tasks using a custom function.
        
        Args:
            filter_func: Function that takes a Task and returns bool
            
        Returns:
            List of tasks that match the filter
        """
        tasks = self.storage.load()
        return [task for task in tasks if filter_func(task)]
    
    def get_statistics(self) -> dict:
        """
        Get task statistics.
        
        Returns:
            Dictionary with task statistics
        """
        tasks = self.storage.load()
        completed = sum(1 for t in tasks if t.completed)
        pending = len(tasks) - completed
        
        priority_counts = {"low": 0, "medium": 0, "high": 0}
        for task in tasks:
            if task.priority in priority_counts:
                priority_counts[task.priority] += 1
        
        return {
            "total": len(tasks),
            "completed": completed,
            "pending": pending,
            "by_priority": priority_counts
        }
