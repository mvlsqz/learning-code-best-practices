"""
Simple tests demonstrating how SOLID principles enable easy testing.

These tests show how DIP (Dependency Inversion) makes testing easy:
- We can inject InMemoryStorage instead of JSONStorage
- No file I/O during tests
- Fast, isolated, reliable tests
"""
from task_manager.task import Task
from task_manager.service import TaskService
from task_manager.storage import InMemoryStorage
from task_manager.formatter import SimpleFormatter, DetailedFormatter


def test_add_task():
    """Test adding a task - no file I/O needed thanks to DIP!"""
    # Arrange - inject in-memory storage
    storage = InMemoryStorage()
    service = TaskService(storage)
    task = Task(title="Test task", description="Test description", priority="high")
    
    # Act
    service.add_task(task)
    
    # Assert
    tasks = service.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Test task"
    assert tasks[0].priority == "high"
    print("✓ test_add_task passed")


def test_complete_task():
    """Test completing a task"""
    # Arrange
    storage = InMemoryStorage()
    service = TaskService(storage)
    task = Task(title="Test task", priority="medium")
    service.add_task(task)
    
    # Act
    result = service.complete_task_by_index(0)
    
    # Assert
    assert result is True
    tasks = service.get_all_tasks()
    assert tasks[0].completed is True
    print("✓ test_complete_task passed")


def test_delete_task():
    """Test deleting a task"""
    # Arrange
    storage = InMemoryStorage()
    service = TaskService(storage)
    task1 = Task(title="Task 1")
    task2 = Task(title="Task 2")
    service.add_task(task1)
    service.add_task(task2)
    
    # Act
    result = service.delete_task_by_index(0)
    
    # Assert
    assert result is True
    tasks = service.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Task 2"
    print("✓ test_delete_task passed")


def test_search_tasks():
    """Test searching tasks"""
    # Arrange
    storage = InMemoryStorage()
    service = TaskService(storage)
    service.add_task(Task(title="Write documentation", description="API docs"))
    service.add_task(Task(title="Fix bug", description="Authentication issue"))
    service.add_task(Task(title="Update docs", description="Add examples"))
    
    # Act
    results = service.search_tasks("doc")
    
    # Assert
    assert len(results) == 2
    assert any("documentation" in t.title.lower() for t in results)
    assert any("docs" in t.title.lower() for t in results)
    print("✓ test_search_tasks passed")


def test_filter_by_priority():
    """Test filtering tasks by priority"""
    # Arrange
    storage = InMemoryStorage()
    service = TaskService(storage)
    service.add_task(Task(title="Task 1", priority="high"))
    service.add_task(Task(title="Task 2", priority="low"))
    service.add_task(Task(title="Task 3", priority="high"))
    
    # Act
    high_priority = service.filter_tasks(lambda t: t.priority == "high")
    
    # Assert
    assert len(high_priority) == 2
    assert all(t.priority == "high" for t in high_priority)
    print("✓ test_filter_by_priority passed")


def test_statistics():
    """Test task statistics"""
    # Arrange
    storage = InMemoryStorage()
    service = TaskService(storage)
    service.add_task(Task(title="Task 1", priority="high"))
    service.add_task(Task(title="Task 2", priority="medium"))
    service.add_task(Task(title="Task 3", priority="high"))
    service.complete_task_by_index(0)
    
    # Act
    stats = service.get_statistics()
    
    # Assert
    assert stats["total"] == 3
    assert stats["completed"] == 1
    assert stats["pending"] == 2
    assert stats["by_priority"]["high"] == 2
    assert stats["by_priority"]["medium"] == 1
    print("✓ test_statistics passed")


def test_formatters_are_interchangeable():
    """
    Test that formatters can be swapped (LSP in action!)
    Both SimpleFormatter and DetailedFormatter implement ITaskFormatter
    and can be used interchangeably.
    """
    # Arrange
    task = Task(title="Test task", description="Description", priority="high")
    tasks = [task]
    
    # Act - use different formatters
    simple_output = SimpleFormatter().format_tasks(tasks)
    detailed_output = DetailedFormatter().format_tasks(tasks)
    
    # Assert - both produce output
    assert "Test task" in simple_output
    assert "Test task" in detailed_output
    assert len(detailed_output) > len(simple_output)  # Detailed has more info
    print("✓ test_formatters_are_interchangeable passed")


def test_storage_implementations_are_interchangeable():
    """
    Test that storage implementations can be swapped (LSP in action!)
    This is the power of DIP - we can easily swap storage types.
    """
    from task_manager.storage import JSONStorage
    import tempfile
    import os
    
    # Test with InMemoryStorage
    mem_storage = InMemoryStorage()
    mem_service = TaskService(mem_storage)
    task1 = Task(title="Task 1")
    mem_service.add_task(task1)
    mem_tasks = mem_service.get_all_tasks()
    
    # Test with JSONStorage (using temp file)
    import tempfile
    temp_file = tempfile.mktemp(suffix='.json')
    
    try:
        json_storage = JSONStorage(temp_file)
        json_service = TaskService(json_storage)
        task2 = Task(title="Task 2")
        json_service.add_task(task2)
        json_tasks = json_service.get_all_tasks()
        
        # Both work identically from TaskService's perspective
        assert len(mem_tasks) == 1
        assert len(json_tasks) == 1
        print("✓ test_storage_implementations_are_interchangeable passed")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("Running Task Manager Tests")
    print("Demonstrating how SOLID principles enable easy testing")
    print("="*60 + "\n")
    
    test_add_task()
    test_complete_task()
    test_delete_task()
    test_search_tasks()
    test_filter_by_priority()
    test_statistics()
    test_formatters_are_interchangeable()
    test_storage_implementations_are_interchangeable()
    
    print("\n" + "="*60)
    print("All tests passed! ✓")
    print("="*60)
    print("\nKey Observations:")
    print("- Tests are fast (no file I/O for most)")
    print("- Tests are isolated (each uses its own storage)")
    print("- Tests are reliable (no external dependencies)")
    print("- Easy to test thanks to DIP (dependency injection)")
    print("- LSP ensures implementations are truly interchangeable")


if __name__ == "__main__":
    run_all_tests()
