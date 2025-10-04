# Liskov Substitution Principle (LSP)

**"Objects of a superclass should be replaceable with objects of a subclass without breaking the application."** - Barbara Liskov

## What It Means

The Liskov Substitution Principle states that if you have a base class (or interface), you should be able to use any of its derived classes (or implementations) in its place without the program behaving incorrectly.

**Translation**: Subtypes must be substitutable for their base types. If it says it's a duck, it should quack like a duck.

## Why It Matters

**Benefits:**
- ✅ **Reliability** - Code behaves predictably with any implementation
- ✅ **Reusability** - Can swap implementations freely
- ✅ **Polymorphism works** - Can truly code to interfaces
- ✅ **Testability** - Can substitute mocks/stubs easily

**Problems Without LSP:**
- ❌ Need to check types before using objects
- ❌ Unexpected behavior when swapping implementations
- ❌ Breaks polymorphism
- ❌ Fragile code that's hard to maintain

## The LSP Contract

When implementing an interface or extending a class, you must:

1. **Accept the same inputs** (or more general)
2. **Return the same outputs** (or more specific)
3. **Maintain the same behavior** expectations
4. **Don't strengthen preconditions** (requirements before)
5. **Don't weaken postconditions** (guarantees after)
6. **Maintain invariants** (things that are always true)

## Real-World Example: Task Manager

### ✅ Follows LSP

```python
from abc import ABC, abstractmethod
from typing import List

class IStorage(ABC):
    @abstractmethod
    def save(self, tasks: List) -> None:
        """Save tasks. Must not raise exception for valid task list."""
        pass
    
    @abstractmethod
    def load(self) -> List:
        """Load tasks. Must return empty list if no data, not None."""
        pass

class JSONStorage(IStorage):
    def save(self, tasks: List) -> None:
        # Saves to JSON file
        with open(self.filename, 'w') as f:
            json.dump(tasks, f)
    
    def load(self) -> List:
        if not os.path.exists(self.filename):
            return []  # Returns empty list as promised
        with open(self.filename, 'r') as f:
            return json.load(f)

class InMemoryStorage(IStorage):
    def save(self, tasks: List) -> None:
        # Saves to memory
        self._tasks = tasks.copy()
    
    def load(self) -> List:
        return self._tasks.copy()  # Returns list as promised

# Both can be used interchangeably
def process_tasks(storage: IStorage):
    tasks = storage.load()  # Always returns a list (never None!)
    # ... process tasks ...
    storage.save(tasks)      # Always works with valid task list

# Works with either storage type
process_tasks(JSONStorage("tasks.json"))
process_tasks(InMemoryStorage())
```

**Why This Works:**
- Both implementations honor the contract
- Both return lists (not None)
- Both accept the same inputs
- Both can be swapped without breaking code

### ❌ Violates LSP

```python
class IStorage(ABC):
    @abstractmethod
    def load(self) -> List:
        pass

class JSONStorage(IStorage):
    def load(self) -> List:
        if not os.path.exists(self.filename):
            return []  # Returns empty list
        with open(self.filename, 'r') as f:
            return json.load(f)

class DatabaseStorage(IStorage):
    def load(self) -> List:
        if not self.connected:
            return None  # VIOLATION! Contract says return List, not None
        # ... load from database ...

# This breaks!
def count_tasks(storage: IStorage):
    tasks = storage.load()
    return len(tasks)  # Crashes if storage is DatabaseStorage and not connected!

# Unexpected behavior
count_tasks(JSONStorage("tasks.json"))     # Works
count_tasks(DatabaseStorage(connection))   # Crashes! Violates LSP
```

**Problem**: `DatabaseStorage` violates the contract by returning `None` instead of a list.

## Classic LSP Violation: Square-Rectangle Problem

### ❌ Violates LSP

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def set_width(self, width):
        self.width = width
    
    def set_height(self, height):
        self.height = height
    
    def area(self):
        return self.width * self.height

class Square(Rectangle):  # Is-a relationship seems logical...
    def set_width(self, width):
        self.width = width
        self.height = width  # But this breaks expectations!
    
    def set_height(self, height):
        self.width = height
        self.height = height

# This breaks LSP
def resize_rectangle(rect: Rectangle):
    rect.set_width(5)
    rect.set_height(4)
    assert rect.area() == 20  # Expect 5 * 4 = 20

resize_rectangle(Rectangle(3, 3))  # Works: area is 20
resize_rectangle(Square(3))        # FAILS! area is 16, not 20
```

**Problem**: Square changes behavior in a way that breaks the Rectangle contract.

### ✅ Better Design

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Square(Shape):  # Doesn't inherit from Rectangle
    def __init__(self, side):
        self.side = side
    
    def area(self):
        return self.side * self.side

# Now both follow their own contracts
```

## How to Apply LSP

### 1. Honor the Contract
If the interface says "returns a list", always return a list (not None, not something else)

### 2. Don't Strengthen Preconditions
```python
# Bad - strengthens preconditions
class IStorage(ABC):
    def save(self, tasks: List):  # Any list is valid
        pass

class StrictStorage(IStorage):
    def save(self, tasks: List):
        if len(tasks) > 100:  # VIOLATION! Added new requirement
            raise ValueError("Too many tasks")
```

### 3. Don't Weaken Postconditions
```python
# Bad - weakens postconditions
class IStorage(ABC):
    def load(self) -> List[Task]:  # Guarantees List[Task]
        pass

class LazyStorage(IStorage):
    def load(self) -> List[str]:  # VIOLATION! Returns different type
        # Returns task IDs instead of tasks
        pass
```

### 4. Maintain Invariants
If the base class guarantees something is always true, subclasses must maintain that guarantee.

## When to Apply LSP

**Do follow LSP when:**
- ✅ Implementing interfaces or abstract classes
- ✅ Extending base classes with new implementations
- ✅ You want true polymorphism
- ✅ Building frameworks or libraries

**Red flags that LSP might be violated:**
- ⚠️ Need to check types before using objects (`if isinstance(...)`)
- ⚠️ Subclass throws exceptions base class doesn't throw
- ⚠️ Subclass has empty implementations that should do something
- ⚠️ Need special handling for certain implementations

## Trade-offs

**Pros:**
- Reliable, predictable code
- True polymorphism
- Easy to test with mocks
- Implementations are interchangeable

**Cons:**
- Must carefully design contracts
- May need to rethink inheritance hierarchies
- Sometimes the "is-a" relationship is misleading

**Rule of Thumb**: If substituting a subclass for its parent breaks behavior or requires special handling, LSP is violated.

## Practice Exercise

Identify the LSP violation:

```python
class Bird:
    def fly(self):
        return "Flying"

class Penguin(Bird):
    def fly(self):
        raise Exception("Can't fly!")  # Is this an LSP violation?

def make_bird_fly(bird: Bird):
    print(bird.fly())

make_bird_fly(Bird())      # Works
make_bird_fly(Penguin())   # Crashes!
```

**Hint**: Penguins are birds, but not all birds fly. How would you redesign this?

## Summary

- **Core idea**: Subtypes must be fully substitutable for their base types
- **Key rule**: Don't break the contract of the base class/interface
- **Watch for**: Type checking, empty implementations, unexpected exceptions
- **Result**: Reliable, flexible polymorphism
- **Remember**: Just because there's an "is-a" relationship doesn't mean inheritance is right

The Liskov Substitution Principle ensures that your abstractions actually work. When you code to an interface, any implementation should work without surprises. This is what makes polymorphism truly powerful and reliable.
