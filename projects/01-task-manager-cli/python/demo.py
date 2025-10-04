#!/usr/bin/env python3
"""
Demo script showing Task Manager CLI capabilities.
This demonstrates all SOLID principles in action.
"""
import os
import sys

# Clean up any existing tasks file for demo
if os.path.exists("demo_tasks.json"):
    os.remove("demo_tasks.json")

from task_manager.task import Task
from task_manager.service import TaskService
from task_manager.storage import JSONStorage
from task_manager.formatter import SimpleFormatter, DetailedFormatter, StatisticsFormatter


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def demo():
    """Run the demo"""
    print_section("Task Manager CLI - SOLID Principles Demo")
    
    # === DEPENDENCY INJECTION (DIP) ===
    print("Creating components with dependency injection...")
    storage = JSONStorage("demo_tasks.json")
    service = TaskService(storage)
    formatter = SimpleFormatter()
    print("✓ Storage, service, and formatter created\n")
    
    # === SINGLE RESPONSIBILITY PRINCIPLE (SRP) ===
    print_section("SRP: Each class has ONE responsibility")
    print("- Task: Represents task data")
    print("- TaskService: Manages business logic")
    print("- JSONStorage: Handles file I/O")
    print("- TaskFormatter: Formats output")
    
    # === Add some tasks ===
    print_section("Adding Tasks")
    tasks_to_add = [
        Task(title="Learn SOLID principles", 
             description="Study all 5 principles with examples", 
             priority="high",
             due_date="2025-10-10"),
        Task(title="Implement Task Manager CLI",
             description="Build CLI demonstrating SOLID",
             priority="high",
             due_date="2025-10-15"),
        Task(title="Write documentation",
             description="Document SOLID principles in code",
             priority="medium"),
        Task(title="Code review",
             description="Review implementation with team",
             priority="low"),
    ]
    
    for task in tasks_to_add:
        service.add_task(task)
        print(f"✓ Added: {task.title}")
    
    # === Display tasks ===
    print_section("Listing All Tasks (Simple Format)")
    tasks = service.get_all_tasks()
    print(formatter.format_tasks(tasks))
    
    # === OPEN/CLOSED PRINCIPLE (OCP) ===
    print_section("OCP: Extension without modification")
    print("Switching to DetailedFormatter without modifying TaskService...")
    detailed_formatter = DetailedFormatter()
    print(detailed_formatter.format_tasks(tasks[:1]))  # Show first task
    print("\n✓ Swapped formatter without changing TaskService!")
    
    # === Complete some tasks ===
    print_section("Completing Tasks")
    service.complete_task_by_index(0)
    print("✓ Completed task 0: Learn SOLID principles")
    service.complete_task_by_index(1)
    print("✓ Completed task 1: Implement Task Manager CLI")
    
    # === LISKOV SUBSTITUTION PRINCIPLE (LSP) ===
    print_section("LSP: Storage implementations are interchangeable")
    print("Currently using JSONStorage")
    print(f"Tasks are persisted to: {storage.filename}")
    
    from task_manager.storage import InMemoryStorage
    print("\nCould easily swap to InMemoryStorage:")
    print("  storage = InMemoryStorage()  # Same interface!")
    print("  service = TaskService(storage)")
    print("✓ Both implement IStorage and work identically")
    
    # === INTERFACE SEGREGATION PRINCIPLE (ISP) ===
    print_section("ISP: Small, focused interfaces")
    print("IStorage interface has only 2 methods:")
    print("  - save(tasks)")
    print("  - load()")
    print("\nITaskFormatter interface has only 1 method:")
    print("  - format_tasks(tasks)")
    print("\n✓ Clients only depend on methods they use")
    
    # === DEPENDENCY INVERSION PRINCIPLE (DIP) ===
    print_section("DIP: Depend on abstractions")
    print("TaskService depends on IStorage (abstraction)")
    print("  NOT on JSONStorage (concrete implementation)")
    print("\nThis enables:")
    print("  ✓ Easy testing (inject mocks)")
    print("  ✓ Flexibility (swap implementations)")
    print("  ✓ Loose coupling")
    
    # === Search and filter ===
    print_section("Searching Tasks")
    results = service.search_tasks("SOLID")
    print(f"Found {len(results)} task(s) with 'SOLID':")
    print(formatter.format_tasks(results))
    
    # === Statistics ===
    print_section("Task Statistics")
    stats = service.get_statistics()
    stats_formatter = StatisticsFormatter()
    print(stats_formatter.format_statistics(stats))
    
    # === Show updated list ===
    print_section("Final Task List")
    tasks = service.get_all_tasks()
    print(formatter.format_tasks(tasks))
    
    # === Summary ===
    print_section("SOLID Principles Summary")
    print("✓ SRP: Each class has single responsibility")
    print("✓ OCP: Can add new storage/formatters without modifying existing code")
    print("✓ LSP: Storage implementations are interchangeable")
    print("✓ ISP: Small, focused interfaces")
    print("✓ DIP: Depend on abstractions, use dependency injection")
    print("\nResult: Maintainable, testable, extensible code! 🎉")
    print("\n" + "="*60 + "\n")
    
    # Clean up demo file
    if os.path.exists("demo_tasks.json"):
        os.remove("demo_tasks.json")
        print("Demo complete. Cleaned up demo_tasks.json")


if __name__ == "__main__":
    demo()
