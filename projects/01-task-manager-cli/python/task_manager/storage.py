"""
Storage Module - Demonstrates OCP, LSP, ISP, and DIP

OCP (Open/Closed Principle): New storage types can be added without modifying existing code
LSP (Liskov Substitution Principle): All storage implementations are interchangeable
ISP (Interface Segregation Principle): Small, focused interface for storage
DIP (Dependency Inversion Principle): High-level code depends on IStorage abstraction
"""
from abc import ABC, abstractmethod
from typing import List
import json
import os
from task_manager.task import Task


class IStorage(ABC):
    """
    Storage interface - demonstrates ISP and DIP.
    
    ISP: This is a small, focused interface with only essential methods.
    DIP: Other components depend on this abstraction, not concrete implementations.
    """
    
    @abstractmethod
    def save(self, tasks: List[Task]) -> None:
        """Save tasks to storage."""
        pass
    
    @abstractmethod
    def load(self) -> List[Task]:
        """Load tasks from storage."""
        pass


class JSONStorage(IStorage):
    """
    JSON file storage implementation.
    
    OCP: This implementation can be used without modifying TaskService.
    LSP: This can be substituted anywhere IStorage is expected.
    SRP: Responsible ONLY for JSON file operations.
    """
    
    def __init__(self, filename: str = "tasks.json"):
        """Initialize with storage filename."""
        self.filename = filename
    
    def save(self, tasks: List[Task]) -> None:
        """Save tasks to JSON file."""
        try:
            data = [task.to_dict() for task in tasks]
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise IOError(f"Failed to save tasks to {self.filename}: {e}")
    
    def load(self) -> List[Task]:
        """Load tasks from JSON file."""
        if not os.path.exists(self.filename):
            return []
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Task.from_dict(item) for item in data]
        except (IOError, json.JSONDecodeError) as e:
            raise IOError(f"Failed to load tasks from {self.filename}: {e}")


class InMemoryStorage(IStorage):
    """
    In-memory storage for testing.
    
    OCP: Adding this didn't require modifying existing code.
    LSP: Can be substituted for JSONStorage without issues.
    """
    
    def __init__(self):
        """Initialize empty task list."""
        self._tasks: List[Task] = []
    
    def save(self, tasks: List[Task]) -> None:
        """Store tasks in memory."""
        self._tasks = tasks.copy()
    
    def load(self) -> List[Task]:
        """Retrieve tasks from memory."""
        return self._tasks.copy()
