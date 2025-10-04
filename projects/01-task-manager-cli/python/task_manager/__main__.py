"""
Main entry point for the Task Manager CLI.

This demonstrates Dependency Inversion Principle (DIP):
- We wire up dependencies here
- Each component depends on abstractions, not concrete classes
"""
from task_manager.cli import TaskCLI
from task_manager.service import TaskService
from task_manager.storage import JSONStorage
from task_manager.formatter import SimpleFormatter


def main():
    """
    Bootstrap the application with dependency injection.
    
    DIP: We create and inject dependencies here.
    This is the only place that knows about concrete implementations.
    """
    # Create storage (can easily swap to InMemoryStorage for testing)
    storage = JSONStorage("tasks.json")
    
    # Create service with storage dependency
    service = TaskService(storage)
    
    # Create formatter (can easily swap to DetailedFormatter)
    formatter = SimpleFormatter()
    
    # Create CLI with all dependencies
    cli = TaskCLI(service, formatter)
    
    # Run the CLI
    cli.run()


if __name__ == "__main__":
    main()
