# Open/Closed Principle (OCP)

**"Software entities should be open for extension but closed for modification."** - Bertrand Meyer

## What It Means

The Open/Closed Principle states that you should be able to add new functionality to existing code without modifying that code. In other words:
- **Open for extension**: You can add new behavior
- **Closed for modification**: You don't change existing code

**Translation**: Write code that can be extended without being modified.

## Why It Matters

**Benefits:**
- ✅ **Reduces risk** - Not modifying working code means less chance of introducing bugs
- ✅ **Easier to maintain** - New features don't require changing existing code
- ✅ **Better stability** - Tested code remains unchanged
- ✅ **Supports growth** - System can grow without becoming fragile

**Problems Without OCP:**
- ❌ Every new feature requires modifying existing code
- ❌ Risk of breaking working functionality
- ❌ Difficult to add features without side effects
- ❌ Code becomes increasingly fragile over time

## How to Achieve OCP

### 1. Use Abstraction (Interfaces/Abstract Classes)

```python
from abc import ABC, abstractmethod

class IStorage(ABC):
    @abstractmethod
    def save(self, data): pass
    
    @abstractmethod
    def load(self): pass

# Add new storage WITHOUT modifying existing code
class JSONStorage(IStorage):
    def save(self, data):
        # JSON implementation
        pass
    
    def load(self):
        # JSON implementation
        pass

class DatabaseStorage(IStorage):  # New! Didn't modify JSONStorage
    def save(self, data):
        # Database implementation
        pass
    
    def load(self):
        # Database implementation
        pass
```

### 2. Use Strategy Pattern

```python
class PaymentProcessor:
    def __init__(self, payment_method):
        self.payment_method = payment_method
    
    def process(self, amount):
        return self.payment_method.pay(amount)

# Add new payment methods without modifying PaymentProcessor
class CreditCardPayment:
    def pay(self, amount):
        # Process credit card
        pass

class PayPalPayment:  # New! Didn't modify PaymentProcessor
    def pay(self, amount):
        # Process PayPal
        pass
```

## Real-World Example: Task Manager

### ❌ Violates OCP

```python
class TaskManager:
    def save_tasks(self, tasks, format_type):
        if format_type == "json":
            # JSON saving logic
            with open("tasks.json", 'w') as f:
                json.dump(tasks, f)
        elif format_type == "xml":
            # XML saving logic
            # ...
        elif format_type == "csv":  # Adding this required modifying this method!
            # CSV saving logic
            # ...
```

**Problem**: Every new format requires modifying the `save_tasks` method.

### ✅ Follows OCP

```python
from abc import ABC, abstractmethod

class IStorage(ABC):
    @abstractmethod
    def save(self, tasks): pass
    
    @abstractmethod
    def load(self): pass

class JSONStorage(IStorage):
    def save(self, tasks):
        with open("tasks.json", 'w') as f:
            json.dump(tasks, f)
    
    def load(self):
        with open("tasks.json", 'r') as f:
            return json.load(f)

class CSVStorage(IStorage):  # Add new format WITHOUT modifying existing code!
    def save(self, tasks):
        # CSV implementation
        pass
    
    def load(self):
        # CSV implementation
        pass

class TaskManager:
    def __init__(self, storage: IStorage):
        self.storage = storage
    
    def save_tasks(self, tasks):
        self.storage.save(tasks)  # Works with ANY storage type!
```

**Benefits**: Can add `XMLStorage`, `DatabaseStorage`, etc. without touching `TaskManager`.

## Common Patterns That Support OCP

### Strategy Pattern
Different algorithms/behaviors can be swapped

### Template Method Pattern
Base behavior is defined, specific steps are overridden

### Decorator Pattern
New functionality is wrapped around existing objects

### Factory Pattern
Object creation is abstracted, new types can be added

## When to Apply OCP

**Do apply OCP when:**
- ✅ You anticipate multiple implementations of similar behavior
- ✅ You're building a framework or library
- ✅ The code is stable and shouldn't be modified often
- ✅ You want to support plugins or extensions

**Don't over-apply:**
- ❌ For code that truly only needs one implementation
- ❌ When abstraction adds unnecessary complexity
- ❌ In prototype/throwaway code

## Trade-offs

**Pros:**
- More stable, less risky changes
- Easier to add features
- Better testability
- Code is more modular

**Cons:**
- More abstract, potentially harder to understand initially
- More classes/files to manage
- Need to predict extension points (not always obvious)

**Rule of Thumb**: If you find yourself modifying the same code repeatedly to add features, it probably violates OCP. Use abstraction to make it extensible instead.

## Practice Exercise

Refactor this code to follow OCP:

```python
class Report:
    def generate(self, data, format):
        if format == "html":
            return f"<html><body>{data}</body></html>"
        elif format == "pdf":
            return f"PDF: {data}"
        elif format == "text":
            return data
```

**Hint**: Create an interface for formatters and separate formatter classes!

## Summary

- **Open for extension**: Add new behavior through new code
- **Closed for modification**: Don't change existing working code
- **Key technique**: Use abstractions (interfaces/abstract classes)
- **Result**: More stable, extensible systems
- **Watch out**: Don't over-abstract simple code

The Open/Closed Principle is about making systems that can grow without becoming fragile. By coding to interfaces and using patterns like Strategy, you create extension points that allow new features without touching working code.
