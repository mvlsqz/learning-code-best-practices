# Dependency Inversion Principle (DIP)

**"Depend upon abstractions, not concretions."** - Robert C. Martin

## What It Means

The Dependency Inversion Principle has two parts:
1. **High-level modules should not depend on low-level modules**. Both should depend on abstractions.
2. **Abstractions should not depend on details**. Details should depend on abstractions.

**Translation**: Code should depend on interfaces/abstractions, not concrete implementations. Dependencies should be "inverted" by injecting them.

## Why It Matters

**Benefits:**
- ✅ **Testability** - Can inject mock dependencies
- ✅ **Flexibility** - Easy to swap implementations
- ✅ **Loose coupling** - Modules are independent
- ✅ **Maintainability** - Changes don't ripple through the system

**Problems Without DIP:**
- ❌ Tight coupling between modules
- ❌ Hard to test (can't mock dependencies)
- ❌ Difficult to change implementations
- ❌ Inflexible, rigid code

## The Dependency Problem

### ❌ Violates DIP (Direct Dependency)

```python
class JSONStorage:
    """Low-level module - handles file operations"""
    def save(self, data):
        with open("data.json", 'w') as f:
            json.dump(data, f)
    
    def load(self):
        with open("data.json", 'r') as f:
            return json.load(f)

class TaskService:
    """High-level module - business logic"""
    def __init__(self):
        # PROBLEM: Depends directly on JSONStorage (concrete class)
        self.storage = JSONStorage()
    
    def add_task(self, task):
        tasks = self.storage.load()
        tasks.append(task)
        self.storage.save(tasks)
```

**Problems:**
- `TaskService` is tightly coupled to `JSONStorage`
- Can't use a different storage without modifying `TaskService`
- Can't test `TaskService` without actual file I/O
- If `JSONStorage` changes, `TaskService` might break

### ✅ Follows DIP (Dependency Injection)

```python
from abc import ABC, abstractmethod

# Abstraction - both high and low-level modules depend on this
class IStorage(ABC):
    @abstractmethod
    def save(self, data): pass
    
    @abstractmethod
    def load(self): pass

# Low-level module depends on abstraction
class JSONStorage(IStorage):
    def save(self, data):
        with open("data.json", 'w') as f:
            json.dump(data, f)
    
    def load(self):
        with open("data.json", 'r') as f:
            return json.load(f)

# Another low-level module depends on same abstraction
class DatabaseStorage(IStorage):
    def save(self, data):
        # Save to database
        pass
    
    def load(self):
        # Load from database
        pass

# High-level module depends on abstraction
class TaskService:
    def __init__(self, storage: IStorage):
        # Dependency is INJECTED, not created internally
        self.storage = storage
    
    def add_task(self, task):
        tasks = self.storage.load()
        tasks.append(task)
        self.storage.save(tasks)

# Wire up dependencies (Dependency Injection)
storage = JSONStorage()  # Choose implementation here
service = TaskService(storage)  # Inject dependency

# Easy to test with mock
mock_storage = MockStorage()
test_service = TaskService(mock_storage)

# Easy to swap implementation
db_storage = DatabaseStorage()
service = TaskService(db_storage)  # Just change this!
```

**Benefits:**
- `TaskService` doesn't know or care about `JSONStorage`
- Can swap storage easily
- Can test with mock storage
- Loose coupling

## Dependency Injection Patterns

### 1. Constructor Injection (Recommended)

```python
class TaskService:
    def __init__(self, storage: IStorage):
        """Dependency injected via constructor"""
        self.storage = storage

# Usage
service = TaskService(JSONStorage())
```

**Pros**: Dependencies are clear, immutable, required

### 2. Property/Setter Injection

```python
class TaskService:
    def set_storage(self, storage: IStorage):
        """Dependency injected via setter"""
        self.storage = storage

# Usage
service = TaskService()
service.set_storage(JSONStorage())
```

**Pros**: Optional dependencies, can change at runtime
**Cons**: Object might be used before dependency is set

### 3. Method Injection

```python
class TaskService:
    def add_task(self, task, storage: IStorage):
        """Dependency injected per method call"""
        tasks = storage.load()
        tasks.append(task)
        storage.save(tasks)

# Usage
service = TaskService()
service.add_task(task, JSONStorage())
```

**Pros**: Different implementation per call
**Cons**: Repetitive, dependency not owned by class

## Real-World Example: Task Manager

### Complete Example

```python
from abc import ABC, abstractmethod

# === ABSTRACTIONS (Interfaces) ===

class IStorage(ABC):
    @abstractmethod
    def save(self, tasks): pass
    
    @abstractmethod
    def load(self): pass

class IFormatter(ABC):
    @abstractmethod
    def format_tasks(self, tasks): pass

# === LOW-LEVEL MODULES ===

class JSONStorage(IStorage):
    def save(self, tasks):
        # JSON implementation
        pass
    
    def load(self):
        # JSON implementation
        pass

class SimpleFormatter(IFormatter):
    def format_tasks(self, tasks):
        # Simple formatting
        pass

# === HIGH-LEVEL MODULES ===

class TaskService:
    """Business logic - depends on IStorage abstraction"""
    def __init__(self, storage: IStorage):
        self.storage = storage  # Injected dependency
    
    def add_task(self, task):
        tasks = self.storage.load()
        tasks.append(task)
        self.storage.save(tasks)

class TaskCLI:
    """UI layer - depends on TaskService and IFormatter abstractions"""
    def __init__(self, service: TaskService, formatter: IFormatter):
        self.service = service    # Injected dependency
        self.formatter = formatter  # Injected dependency
    
    def display_tasks(self):
        tasks = self.service.get_all_tasks()
        print(self.formatter.format_tasks(tasks))

# === DEPENDENCY WIRING (Composition Root) ===

def main():
    """
    This is the only place that knows about concrete implementations.
    This is where we "invert" the dependencies.
    """
    # Create low-level modules
    storage = JSONStorage("tasks.json")
    formatter = SimpleFormatter()
    
    # Inject into high-level modules
    service = TaskService(storage)
    cli = TaskCLI(service, formatter)
    
    # Run application
    cli.run()
```

## DIP vs Dependency Injection

**Dependency Inversion Principle (DIP)**:
- A design principle
- About depending on abstractions
- About the direction of dependencies

**Dependency Injection (DI)**:
- A design pattern/technique
- A way to achieve DIP
- About how objects get their dependencies

**Relationship**: Dependency Injection is one way to implement Dependency Inversion Principle.

## Benefits for Testing

### Without DIP
```python
class TaskService:
    def __init__(self):
        self.storage = JSONStorage()  # Hard to test!
    
    def add_task(self, task):
        # Tests will do actual file I/O
        pass

# Testing requires real file system
def test_add_task():
    service = TaskService()
    # Creates actual files!
    service.add_task(task)
```

### With DIP
```python
class TaskService:
    def __init__(self, storage: IStorage):
        self.storage = storage  # Can inject mock!
    
    def add_task(self, task):
        # Can test without file I/O
        pass

# Testing with mock
class MockStorage(IStorage):
    def __init__(self):
        self.data = []
    
    def save(self, data):
        self.data = data
    
    def load(self):
        return self.data

def test_add_task():
    mock = MockStorage()
    service = TaskService(mock)  # Inject mock
    service.add_task(task)
    # No file I/O, fast tests!
    assert len(mock.data) == 1
```

## Dependency Direction

### Traditional (Without DIP)
```
┌─────────────────┐
│  TaskService    │  (high-level)
│  (business)     │
└────────┬────────┘
         │ depends on
         ↓
┌────────┴────────┐
│  JSONStorage    │  (low-level)
│  (details)      │
└─────────────────┘
```

High-level depends on low-level (bad!)

### Inverted (With DIP)
```
┌─────────────────┐
│  TaskService    │  (high-level)
│  (business)     │
└────────┬────────┘
         │ depends on
         ↓
┌────────┴────────┐
│   IStorage      │  (abstraction)
│  (interface)    │
└────────┬────────┘
         ↑ depends on
         │
┌────────┴────────┐
│  JSONStorage    │  (low-level)
│  (details)      │
└─────────────────┘
```

Both depend on abstraction (good!)

## When to Apply DIP

**Do apply DIP when:**
- ✅ Building testable code
- ✅ Anticipating multiple implementations
- ✅ High-level logic shouldn't know low-level details
- ✅ Want flexibility to change implementations

**Don't over-apply:**
- ❌ For truly simple, one-implementation scenarios
- ❌ When abstraction adds no value
- ❌ In prototypes or throwaway code

## Trade-offs

**Pros:**
- Testable (can mock dependencies)
- Flexible (easy to swap implementations)
- Loose coupling
- Clear separation of concerns

**Cons:**
- More abstract, potentially harder to follow
- More interfaces to manage
- Requires understanding of DI

**Rule of Thumb**: If you find it hard to test a class, it probably violates DIP. If changing a low-level detail breaks high-level code, it violates DIP.

## Common Mistakes

### 1. Creating Dependencies Inside

```python
# BAD
class TaskService:
    def __init__(self):
        self.storage = JSONStorage()  # Created internally

# GOOD
class TaskService:
    def __init__(self, storage: IStorage):
        self.storage = storage  # Injected
```

### 2. Depending on Concrete Types

```python
# BAD
class TaskService:
    def __init__(self, storage: JSONStorage):  # Concrete type
        self.storage = storage

# GOOD
class TaskService:
    def __init__(self, storage: IStorage):  # Abstract type
        self.storage = storage
```

### 3. No Abstraction Layer

```python
# BAD - no abstraction
class TaskService:
    def __init__(self, storage):
        self.storage = storage  # No contract defined

# GOOD - has abstraction
class TaskService:
    def __init__(self, storage: IStorage):  # Contract defined
        self.storage = storage
```

## Practice Exercise

Refactor this code to follow DIP:

```python
class EmailService:
    def send(self, to, subject, body):
        # Send via SMTP
        pass

class NotificationService:
    def __init__(self):
        self.email = EmailService()  # Direct dependency!
    
    def notify_user(self, user, message):
        self.email.send(user.email, "Notification", message)
```

**Hint**: Create an `IMessageSender` interface and inject it!

## Summary

- **Core idea**: Depend on abstractions, not concretions
- **Key technique**: Dependency Injection (constructor injection preferred)
- **Benefits**: Testability, flexibility, loose coupling
- **Watch for**: Creating dependencies inside classes
- **Result**: Maintainable, adaptable systems

The Dependency Inversion Principle is arguably the most powerful SOLID principle. It enables testability, flexibility, and maintainability by ensuring that high-level code doesn't depend on low-level implementation details. Master this principle, and your code will be much easier to work with.

**Remember**: "New is Glue" - creating objects with `new` (or direct instantiation) creates tight coupling. Inject dependencies instead.
