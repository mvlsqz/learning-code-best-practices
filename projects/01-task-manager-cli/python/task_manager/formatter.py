"""
Formatters - Demonstrates SRP and ISP

SRP: Each formatter has ONE responsibility - format output in a specific way.
ISP: Small, focused interface for formatting.
"""
from abc import ABC, abstractmethod
from typing import List
from task_manager.task import Task


class ITaskFormatter(ABC):
    """
    Formatter interface.
    
    ISP: Small, focused interface with single method.
    DIP: CLI depends on this abstraction, not concrete formatters.
    """
    
    @abstractmethod
    def format_tasks(self, tasks: List[Task]) -> str:
        """Format a list of tasks for display."""
        pass


class SimpleFormatter(ITaskFormatter):
    """
    Simple text formatter.
    
    SRP: Responsible ONLY for simple text formatting.
    OCP: Can be extended or replaced without modifying other code.
    """
    
    def format_tasks(self, tasks: List[Task]) -> str:
        """Format tasks as simple text list."""
        if not tasks:
            return "No tasks found."
        
        lines = []
        for i, task in enumerate(tasks):
            status = "✓" if task.completed else " "
            priority_symbol = {
                "low": "↓",
                "medium": "→",
                "high": "↑"
            }.get(task.priority, "→")
            
            line = f"[{status}] {i}. {priority_symbol} {task.title}"
            if task.description:
                line += f" - {task.description}"
            if task.due_date:
                line += f" (Due: {task.due_date})"
            lines.append(line)
        
        return "\n".join(lines)


class DetailedFormatter(ITaskFormatter):
    """
    Detailed formatter showing all task information.
    
    SRP: Responsible ONLY for detailed formatting.
    OCP: Adding this didn't require modifying existing code.
    """
    
    def format_tasks(self, tasks: List[Task]) -> str:
        """Format tasks with detailed information."""
        if not tasks:
            return "No tasks found."
        
        lines = []
        for i, task in enumerate(tasks):
            status = "Completed" if task.completed else "Pending"
            lines.append(f"\n{'='*60}")
            lines.append(f"Task #{i} (ID: {task.id})")
            lines.append(f"{'='*60}")
            lines.append(f"Title:       {task.title}")
            lines.append(f"Description: {task.description}")
            lines.append(f"Priority:    {task.priority.upper()}")
            lines.append(f"Status:      {status}")
            lines.append(f"Due Date:    {task.due_date or 'Not set'}")
            lines.append(f"Created:     {task.created_at}")
        
        return "\n".join(lines)


class StatisticsFormatter:
    """
    Formats task statistics.
    
    SRP: Responsible ONLY for formatting statistics.
    """
    
    def format_statistics(self, stats: dict) -> str:
        """Format statistics dictionary."""
        lines = [
            "\n" + "="*40,
            "Task Statistics",
            "="*40,
            f"Total Tasks:      {stats['total']}",
            f"Completed:        {stats['completed']}",
            f"Pending:          {stats['pending']}",
            "",
            "By Priority:",
            f"  High:           {stats['by_priority']['high']}",
            f"  Medium:         {stats['by_priority']['medium']}",
            f"  Low:            {stats['by_priority']['low']}",
            "="*40
        ]
        return "\n".join(lines)
