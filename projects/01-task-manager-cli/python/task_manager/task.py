"""
Task Model - Demonstrates Single Responsibility Principle (SRP)

This class has ONE responsibility: Represent a task's data.
It doesn't handle storage, formatting, or business logic.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Task:
    """
    Represents a single task in the task management system.
    
    SRP: This class is responsible ONLY for holding task data.
    It does not:
    - Save/load tasks (that's Storage's job)
    - Format output (that's Formatter's job)
    - Manage task collections (that's TaskService's job)
    """
    title: str
    description: str = ""
    priority: str = "medium"  # low, medium, high
    due_date: Optional[str] = None
    completed: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def __post_init__(self):
        """Validate priority values."""
        valid_priorities = ["low", "medium", "high"]
        if self.priority not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
    
    def to_dict(self) -> dict:
        """Convert task to dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "completed": self.completed,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create Task instance from dictionary."""
        return cls(**data)
