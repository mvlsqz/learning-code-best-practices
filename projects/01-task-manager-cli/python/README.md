# Task Manager CLI - Python Implementation

A command-line task management application demonstrating all 5 SOLID principles.

## 🎯 SOLID Principles Demonstrated

### 1. Single Responsibility Principle (SRP)
Each class has ONE clear responsibility:
- **Task**: Represents task data
- **TaskService**: Manages task business logic
- **JSONStorage**: Handles file I/O
- **TaskFormatter**: Formats output
- **TaskCLI**: Handles CLI interaction

### 2. Open/Closed Principle (OCP)
The system is open for extension, closed for modification:
- New storage types can be added (e.g., `DatabaseStorage`) without modifying `TaskService`
- New formatters can be added without modifying `TaskCLI`
- New commands can be added without changing existing code

### 3. Liskov Substitution Principle (LSP)
All implementations are interchangeable:
- `JSONStorage` and `InMemoryStorage` can be swapped without breaking `TaskService`
- `SimpleFormatter` and `DetailedFormatter` can be swapped without breaking `TaskCLI`

### 4. Interface Segregation Principle (ISP)
Small, focused interfaces:
- `IStorage`: Only 2 methods (save, load)
- `ITaskFormatter`: Only 1 method (format_tasks)
- Clients only depend on methods they use

### 5. Dependency Inversion Principle (DIP)
High-level modules depend on abstractions:
- `TaskService` depends on `IStorage` interface, not `JSONStorage`
- `TaskCLI` depends on `ITaskFormatter` interface, not concrete formatters
- Dependencies are injected via constructors

## 📦 Installation

```bash
cd projects/01-task-manager-cli/python
# No additional dependencies needed - uses Python standard library only!
```

## 🚀 Usage

### Basic Commands

```bash
# Add a task
python task.py add "Write documentation" --description "Complete API docs" --priority high --due "2025-10-10"

# List all tasks
python task.py list

# List with filters
python task.py list --status pending
python task.py list --priority high
python task.py list --detailed

# Mark task as complete
python task.py complete 0

# Update a task
python task.py update 0 --priority medium --description "Updated description"

# Delete a task
python task.py delete 0

# Search tasks
python task.py search "documentation"

# Show statistics
python task.py stats
```

### Using as a Module

```bash
python -m task_manager add "My task"
python -m task_manager list
```

## 📁 Project Structure

```
python/
├── task_manager/
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # Entry point with dependency injection
│   ├── task.py              # Task model (SRP)
│   ├── storage.py           # Storage interfaces and implementations (OCP, LSP, ISP, DIP)
│   ├── service.py           # Business logic (SRP, DIP)
│   ├── formatter.py         # Output formatters (SRP, ISP, OCP)
│   └── cli.py               # CLI interface (SRP, DIP)
├── task.py                  # Convenience script
└── README.md                # This file
```

## 🧪 Testing

The code is designed to be easily testable thanks to SOLID principles:

```python
from task_manager.service import TaskService
from task_manager.storage import InMemoryStorage
from task_manager.task import Task

# Easy to test with in-memory storage (DIP in action!)
storage = InMemoryStorage()
service = TaskService(storage)

task = Task(title="Test task", priority="high")
service.add_task(task)

tasks = service.get_all_tasks()
assert len(tasks) == 1
assert tasks[0].title == "Test task"
```

## 💡 Key Design Decisions

### Why Dependency Injection?
- Makes code testable (can inject mock storage)
- Makes code flexible (easy to swap implementations)
- Demonstrates DIP principle

### Why Interfaces (ABC)?
- Enforces contracts
- Enables LSP (substitutability)
- Documents expected behavior

### Why Small Classes?
- Each class has single responsibility (SRP)
- Easier to understand and maintain
- Easier to test in isolation

### Why Formatters?
- Separates presentation from logic (SRP)
- Easy to add new output formats (OCP)
- CLI doesn't need to know formatting details

## 🔄 Extending the Application

### Adding a New Storage Type

```python
# storage.py
class DatabaseStorage(IStorage):
    def save(self, tasks: List[Task]) -> None:
        # Save to database
        pass
    
    def load(self) -> List[Task]:
        # Load from database
        pass

# __main__.py
storage = DatabaseStorage("connection_string")  # Just change this line!
service = TaskService(storage)
```

### Adding a New Formatter

```python
# formatter.py
class MarkdownFormatter(ITaskFormatter):
    def format_tasks(self, tasks: List[Task]) -> str:
        # Format as markdown
        pass

# __main__.py
formatter = MarkdownFormatter()  # Just change this line!
cli = TaskCLI(service, formatter)
```

## 📚 Learning Resources

- See `docs/solid-principles/` for detailed explanations
- Read "Clean Code" by Robert C. Martin
- Visit https://refactoring.guru/design-patterns/solid
