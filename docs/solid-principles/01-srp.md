# Single Responsibility Principle (SRP)

**"A class should have one, and only one, reason to change."** - Robert C. Martin

## What It Means

The Single Responsibility Principle states that every module, class, or function should have responsibility over a single part of the functionality, and that responsibility should be entirely encapsulated by the class.

**Translation**: Each class should do ONE thing and do it well.

## Why It Matters

**Benefits:**
- ✅ **Easier to understand** - Classes with clear, single purposes are easier to comprehend
- ✅ **Easier to test** - Smaller, focused classes are simpler to test
- ✅ **Less coupling** - Changes to one responsibility don't affect others
- ✅ **Better organization** - Code structure becomes clearer
- ✅ **Easier to maintain** - Finding and fixing bugs is simpler

**Problems Without SRP:**
- ❌ Large, complex classes that do too much
- ❌ Changes in one area break unrelated functionality
- ❌ Difficult to test (need to mock too many dependencies)
- ❌ Hard to reuse code in other contexts

## The "Reason to Change" Test

A class violates SRP if you can think of more than one reason to change it.

**Example Questions:**
- Would you change this class if the database changes?
- Would you change this class if the UI format changes?
- Would you change this class if business rules change?

If you answer "yes" to multiple questions, you have multiple responsibilities!

## Examples

### ❌ Bad Example (Violates SRP)

```python
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
    
    def get_user_info(self) -> dict:
        return {"name": self.name, "email": self.email}
    
    def save_to_database(self):
        """PROBLEM: User class knows about database!"""
        db = Database()
        db.execute(f"INSERT INTO users VALUES ('{self.name}', '{self.email}')")
    
    def send_welcome_email(self):
        """PROBLEM: User class knows about email!"""
        email_service = EmailService()
        email_service.send(
            to=self.email,
            subject="Welcome!",
            body=f"Hello {self.name}!"
        )
    
    def generate_report(self) -> str:
        """PROBLEM: User class knows about reporting!"""
        return f"User Report\n" \
               f"Name: {self.name}\n" \
               f"Email: {self.email}"
```

**Why This Is Bad:**

This `User` class has **FOUR** responsibilities:
1. **Data representation** (storing user data)
2. **Database operations** (saving to database)
3. **Email operations** (sending emails)
4. **Report generation** (formatting output)

**Reasons to change:**
- Database schema changes
- Email service provider changes
- Report format changes
- User data structure changes

### ✅ Good Example (Follows SRP)

```python
# Responsibility #1: Represent user data
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
    
    def get_user_info(self) -> dict:
        return {"name": self.name, "email": self.email}

# Responsibility #2: Save/load users from database
class UserRepository:
    def __init__(self, database: Database):
        self.db = database
    
    def save(self, user: User) -> None:
        self.db.execute(
            "INSERT INTO users VALUES (?, ?)",
            (user.name, user.email)
        )
    
    def find_by_email(self, email: str) -> User:
        result = self.db.query("SELECT * FROM users WHERE email = ?", (email,))
        return User(name=result['name'], email=result['email'])

# Responsibility #3: Send emails
class EmailService:
    def send_welcome_email(self, user: User) -> None:
        self.send(
            to=user.email,
            subject="Welcome!",
            body=f"Hello {user.name}!"
        )
    
    def send(self, to: str, subject: str, body: str) -> None:
        # Email sending logic
        pass

# Responsibility #4: Generate reports
class UserReportGenerator:
    def generate(self, user: User) -> str:
        return f"User Report\n" \
               f"Name: {user.name}\n" \
               f"Email: {user.email}"

# Usage
user = User("John Doe", "john@example.com")
repository = UserRepository(database)
repository.save(user)

email_service = EmailService()
email_service.send_welcome_email(user)

report_gen = UserReportGenerator()
print(report_gen.generate(user))
```

**Why This Is Better:**

Each class has **ONE** responsibility:
- `User`: Represents user data
- `UserRepository`: Handles database operations
- `EmailService`: Handles email sending
- `UserReportGenerator`: Handles report formatting

**Benefits:**
- Change database? Only modify `UserRepository`
- Change email provider? Only modify `EmailService`
- Change report format? Only modify `UserReportGenerator`
- Change user fields? Only modify `User` and maybe its dependencies

## Real-World Example: Task Manager

### ❌ Violates SRP

```python
class TaskManager:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, title: str, description: str):
        self.tasks.append({"title": title, "description": description})
    
    def remove_task(self, index: int):
        del self.tasks[index]
    
    def save_to_file(self, filename: str):
        """Database concern mixed with business logic!"""
        with open(filename, 'w') as f:
            json.dump(self.tasks, f)
    
    def load_from_file(self, filename: str):
        """Database concern mixed with business logic!"""
        with open(filename, 'r') as f:
            self.tasks = json.load(f)
    
    def display_tasks(self):
        """UI concern mixed with business logic!"""
        for i, task in enumerate(self.tasks):
            print(f"{i}. {task['title']} - {task['description']}")
    
    def send_task_reminder(self, task_index: int, email: str):
        """Email concern mixed with business logic!"""
        task = self.tasks[task_index]
        # Send email logic...
```

### ✅ Follows SRP

```python
# Data model - represents a task
class Task:
    def __init__(self, title: str, description: str, priority: str = "medium"):
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = False

# Business logic - manages tasks
class TaskService:
    def __init__(self, storage: 'IStorage'):
        self.storage = storage
    
    def add_task(self, task: Task) -> None:
        tasks = self.storage.load()
        tasks.append(task)
        self.storage.save(tasks)
    
    def remove_task(self, task_id: int) -> None:
        tasks = self.storage.load()
        del tasks[task_id]
        self.storage.save(tasks)
    
    def get_all_tasks(self) -> List[Task]:
        return self.storage.load()

# Storage - handles file I/O
class JSONStorage:
    def __init__(self, filename: str):
        self.filename = filename
    
    def save(self, tasks: List[Task]) -> None:
        with open(self.filename, 'w') as f:
            json.dump([t.__dict__ for t in tasks], f)
    
    def load(self) -> List[Task]:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as f:
            data = json.load(f)
            return [Task(**item) for item in data]

# Display - handles formatting
class TaskFormatter:
    def format_list(self, tasks: List[Task]) -> str:
        output = []
        for i, task in enumerate(tasks):
            status = "✓" if task.completed else " "
            output.append(f"[{status}] {i}. {task.title} - {task.description}")
        return "\n".join(output)

# Notifications - handles email
class TaskReminderService:
    def send_reminder(self, task: Task, email: str) -> None:
        # Email sending logic
        pass
```

## TypeScript Example

```typescript
// ❌ Bad - Multiple responsibilities
class UserService {
  createUser(name: string, email: string): User {
    // Create user
    const user = new User(name, email);
    
    // Save to database (responsibility #2)
    this.database.save(user);
    
    // Send email (responsibility #3)
    this.emailService.send(email, "Welcome!");
    
    // Log (responsibility #4)
    console.log(`User ${name} created`);
    
    return user;
  }
}

// ✅ Good - Single responsibility each
class User {
  constructor(public name: string, public email: string) {}
}

class UserRepository {
  save(user: User): void {
    this.database.insert('users', user);
  }
}

class EmailService {
  sendWelcomeEmail(user: User): void {
    this.send(user.email, "Welcome!", `Hello ${user.name}!`);
  }
}

class Logger {
  logUserCreation(user: User): void {
    console.log(`User ${user.name} created at ${new Date()}`);
  }
}

// Orchestrator (this can have multiple dependencies, but delegates work)
class UserService {
  constructor(
    private repository: UserRepository,
    private emailService: EmailService,
    private logger: Logger
  ) {}
  
  createUser(name: string, email: string): User {
    const user = new User(name, email);
    this.repository.save(user);
    this.emailService.sendWelcomeEmail(user);
    this.logger.logUserCreation(user);
    return user;
  }
}
```

## Common Violations

### God Objects
Classes that know too much or do too much.

```python
# ❌ God object - does everything!
class Application:
    def handle_request(self):
        ...
    def connect_database(self):
        ...
    def send_email(self):
        ...
    def generate_pdf(self):
        ...
    def process_payment(self):
        ...
```

### Mixed Concerns
Mixing business logic with infrastructure.

```python
# ❌ Business logic mixed with database code
def calculate_discount(user_id: int) -> float:
    # Database access
    conn = sqlite3.connect('database.db')
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    
    # Business logic
    if user['premium']:
        return 0.20
    return 0.10
```

## How to Apply SRP

### Step 1: Identify Responsibilities
List everything the class does.

### Step 2: Group Related Behaviors
Which behaviors naturally belong together?

### Step 3: Extract Classes
Create new classes for each distinct responsibility.

### Step 4: Use Composition
Connect classes through dependency injection.

## When to Apply SRP

**Do apply SRP when:**
- ✅ A class is becoming large and complex
- ✅ You're mixing different levels of abstraction
- ✅ Testing requires extensive mocking
- ✅ Changes in one area affect unrelated code

**Don't over-apply:**
- ❌ Creating tiny classes for every single method
- ❌ Premature abstraction (wait until you see the pattern)
- ❌ When it makes code harder to understand

## Trade-offs

**Pros:**
- More maintainable code
- Easier testing
- Better organization
- Loose coupling

**Cons:**
- More files/classes to manage
- Slightly more complex to navigate initially
- Need dependency injection

**Rule of Thumb**: If it's hard to name a class without using "and" or "or", it probably has too many responsibilities.

## Practice Exercise

Take this class and refactor it to follow SRP:

```python
class BlogPost:
    def __init__(self, title, content):
        self.title = title
        self.content = content
    
    def save_to_database(self):
        # Save logic
        pass
    
    def display_html(self):
        return f"<h1>{self.title}</h1><p>{self.content}</p>"
    
    def send_notification(self, subscribers):
        for email in subscribers:
            # Send email
            pass
```

**Hint**: Identify at least 4 separate responsibilities!

## Summary

- **One class = One responsibility**
- **One reason to change per class**
- **Separate concerns** (business logic, data access, presentation)
- **Easier to test, maintain, and understand**
- **Don't over-apply** - use common sense

---

**Next**: [Open/Closed Principle](./02-ocp.md)
