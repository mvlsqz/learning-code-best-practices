# Interface Segregation Principle (ISP)

**"No client should be forced to depend on methods it does not use."** - Robert C. Martin

## What It Means

The Interface Segregation Principle states that it's better to have many small, specific interfaces than one large, general-purpose interface. Clients should not be forced to implement methods they don't need.

**Translation**: Keep interfaces small and focused. Don't make classes implement methods they won't use.

## Why It Matters

**Benefits:**
- ✅ **Cleaner code** - Classes only implement what they need
- ✅ **Less coupling** - Changes to unused methods don't affect clients
- ✅ **Easier to understand** - Smaller interfaces are clearer
- ✅ **More flexible** - Can implement multiple small interfaces

**Problems Without ISP:**
- ❌ Fat interfaces with many methods
- ❌ Classes forced to implement empty/dummy methods
- ❌ Unnecessary dependencies
- ❌ More fragile code (changes ripple through)

## Real-World Example: Task Manager

### ❌ Violates ISP

```python
from abc import ABC, abstractmethod

class ITaskManager(ABC):
    """Fat interface - forces implementers to implement everything"""
    
    @abstractmethod
    def save_tasks(self, tasks): pass
    
    @abstractmethod
    def load_tasks(self): pass
    
    @abstractmethod
    def format_tasks(self, tasks): pass
    
    @abstractmethod
    def send_email_notification(self, task): pass
    
    @abstractmethod
    def export_to_pdf(self, tasks): pass
    
    @abstractmethod
    def sync_to_cloud(self, tasks): pass

# This class only needs storage, but must implement everything!
class SimpleStorage(ITaskManager):
    def save_tasks(self, tasks):
        # Actually implement this
        pass
    
    def load_tasks(self):
        # Actually implement this
        pass
    
    def format_tasks(self, tasks):
        raise NotImplementedError("Don't need this!")  # Forced to implement
    
    def send_email_notification(self, task):
        raise NotImplementedError("Don't need this!")  # Forced to implement
    
    def export_to_pdf(self, tasks):
        raise NotImplementedError("Don't need this!")  # Forced to implement
    
    def sync_to_cloud(self, tasks):
        raise NotImplementedError("Don't need this!")  # Forced to implement
```

**Problem**: `SimpleStorage` only needs save/load but must implement 6 methods.

### ✅ Follows ISP

```python
from abc import ABC, abstractmethod

# Small, focused interfaces
class IStorage(ABC):
    """Only storage operations"""
    @abstractmethod
    def save(self, tasks): pass
    
    @abstractmethod
    def load(self): pass

class IFormatter(ABC):
    """Only formatting operations"""
    @abstractmethod
    def format_tasks(self, tasks): pass

class INotifier(ABC):
    """Only notification operations"""
    @abstractmethod
    def send_notification(self, task): pass

class IExporter(ABC):
    """Only export operations"""
    @abstractmethod
    def export_to_pdf(self, tasks): pass

# Now classes only implement what they need
class JSONStorage(IStorage):
    def save(self, tasks):
        # Implementation
        pass
    
    def load(self):
        # Implementation
        pass
    # No need to implement formatting, notifications, etc.

class SimpleFormatter(IFormatter):
    def format_tasks(self, tasks):
        # Implementation
        pass
    # No need to implement storage, notifications, etc.

# Can implement multiple interfaces if needed
class FullFeaturedManager(IStorage, IFormatter, INotifier):
    def save(self, tasks): pass
    def load(self): pass
    def format_tasks(self, tasks): pass
    def send_notification(self, task): pass
    # Still doesn't need to implement IExporter
```

**Benefits**: Each class implements only the interfaces it needs.

## Another Example: Printer Interfaces

### ❌ Violates ISP

```python
class IPrinter(ABC):
    """Fat interface - assumes all printers can do everything"""
    
    @abstractmethod
    def print(self, document): pass
    
    @abstractmethod
    def scan(self, document): pass
    
    @abstractmethod
    def fax(self, document): pass

class SimplePrinter(IPrinter):
    """Just prints, but forced to implement scan and fax!"""
    
    def print(self, document):
        print(f"Printing: {document}")
    
    def scan(self, document):
        raise NotImplementedError("This printer can't scan!")
    
    def fax(self, document):
        raise NotImplementedError("This printer can't fax!")
```

### ✅ Follows ISP

```python
class IPrinter(ABC):
    @abstractmethod
    def print(self, document): pass

class IScanner(ABC):
    @abstractmethod
    def scan(self, document): pass

class IFax(ABC):
    @abstractmethod
    def fax(self, document): pass

class SimplePrinter(IPrinter):
    """Only implements printing"""
    def print(self, document):
        print(f"Printing: {document}")

class MultiFunctionPrinter(IPrinter, IScanner, IFax):
    """Implements all interfaces"""
    def print(self, document):
        print(f"Printing: {document}")
    
    def scan(self, document):
        print(f"Scanning: {document}")
    
    def fax(self, document):
        print(f"Faxing: {document}")
```

## How to Apply ISP

### 1. Split Large Interfaces

```python
# Bad - one large interface
class IDataService(ABC):
    def read(self): pass
    def write(self): pass
    def delete(self): pass
    def validate(self): pass
    def transform(self): pass

# Good - split into focused interfaces
class IReader(ABC):
    def read(self): pass

class IWriter(ABC):
    def write(self): pass

class IValidator(ABC):
    def validate(self): pass
```

### 2. Use Role Interfaces

Design interfaces based on **how they're used** (client perspective), not based on what an object **is**.

```python
# Based on roles/capabilities
class IReadable(ABC):
    def read(self): pass

class IWritable(ABC):
    def write(self): pass

class ICloseable(ABC):
    def close(self): pass

# File can implement multiple role interfaces
class File(IReadable, IWritable, ICloseable):
    pass
```

### 3. Client-Specific Interfaces

Design interfaces for specific client needs:

```python
# Interface for displaying tasks
class ITaskDisplay(ABC):
    def get_title(self): pass
    def get_status(self): pass

# Interface for storage
class ITaskPersistence(ABC):
    def to_dict(self): pass
    def from_dict(self, data): pass

# Task implements both
class Task(ITaskDisplay, ITaskPersistence):
    # Implementation
    pass
```

## ISP and SRP

ISP complements Single Responsibility Principle:
- **SRP**: Classes should have one reason to change
- **ISP**: Interfaces should have one reason to exist

Both push toward smaller, more focused components.

## When to Apply ISP

**Do apply ISP when:**
- ✅ An interface has many methods
- ✅ Clients don't need all methods
- ✅ Implementations have dummy/empty methods
- ✅ Changes to one part affect unrelated clients

**Don't over-apply:**
- ❌ Creating single-method interfaces for everything
- ❌ When all clients truly need all methods
- ❌ In very simple scenarios

## Trade-offs

**Pros:**
- More modular, focused code
- Easier to implement
- Less coupling
- More flexibility

**Cons:**
- More interfaces to manage
- Can be confusing with too many tiny interfaces
- Need to understand which interfaces to implement

**Rule of Thumb**: If you're writing empty implementations or throwing "not supported" exceptions, your interface is probably too large.

## ISP in Different Languages

### Python
```python
# Python uses abstract base classes
from abc import ABC, abstractmethod

class IStorage(ABC):
    @abstractmethod
    def save(self): pass
```

### TypeScript
```typescript
// TypeScript has native interface support
interface IStorage {
  save(tasks: Task[]): void;
  load(): Task[];
}
```

### Java
```java
// Java uses interface keyword
public interface IStorage {
  void save(List<Task> tasks);
  List<Task> load();
}
```

## Practice Exercise

Refactor this fat interface:

```python
class IEmployee(ABC):
    @abstractmethod
    def work(self): pass
    
    @abstractmethod
    def get_salary(self): pass
    
    @abstractmethod
    def manage_team(self): pass  # Not all employees manage!
    
    @abstractmethod
    def do_technical_work(self): pass  # Not all employees do technical work!
```

**Hint**: Split into `IWorker`, `IManager`, `IEngineer`, etc.

## Common Patterns That Support ISP

### Multiple Inheritance/Implementation
```python
class Task(IDisplayable, IPersistable, ISearchable):
    # Implements multiple focused interfaces
    pass
```

### Adapter Pattern
```python
# Adapt a fat interface to a thin one
class StorageAdapter(IStorage):
    def __init__(self, fat_interface):
        self.interface = fat_interface
    
    def save(self, tasks):
        self.interface.save_tasks(tasks)
```

## Summary

- **Core idea**: Many small interfaces > one large interface
- **Key benefit**: Clients only depend on what they use
- **Watch for**: Empty implementations, "not supported" errors
- **Result**: More modular, flexible code
- **Remember**: Design interfaces from the client's perspective

The Interface Segregation Principle is about respecting your clients. Don't force them to depend on things they don't need. Small, focused interfaces lead to cleaner, more maintainable code.

**Quote**: "Make interfaces easy to use correctly and hard to use incorrectly." - Scott Meyers
