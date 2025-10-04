# Task Manager CLI - Quick Start Guide

Get started with the Task Manager CLI in 5 minutes!

## 🚀 Installation

No installation needed! Just Python 3.8+ required.

```bash
cd projects/01-task-manager-cli/python
```

## 📝 Basic Usage

### Add Tasks
```bash
python task.py add "My first task" --description "Getting started" --priority high
```

### List Tasks
```bash
python task.py list
```

### Complete a Task
```bash
python task.py complete 0
```

### See Statistics
```bash
python task.py stats
```

## 🎯 Quick Demo

Run the interactive demo to see all features:
```bash
python demo.py
```

Run the test suite:
```bash
python test_task_manager.py
```

## 📚 Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add` | Add a new task | `python task.py add "Task title" --priority high` |
| `list` | List all tasks | `python task.py list --status pending` |
| `complete` | Mark task complete | `python task.py complete 0` |
| `update` | Update task details | `python task.py update 0 --priority low` |
| `delete` | Delete a task | `python task.py delete 0` |
| `search` | Search tasks | `python task.py search "keyword"` |
| `stats` | Show statistics | `python task.py stats` |

## 🎓 Learning Resources

- [SOLID Principles Explanation](./python/SOLID_PRINCIPLES.md) - How each principle is applied
- [Complete README](./python/README.md) - Full documentation
- [SOLID Principles Guide](../../docs/solid-principles/) - Detailed principle explanations

## 💡 What Makes This Special?

This isn't just a task manager - it's a learning tool that demonstrates:

✅ **Clean Architecture** - Well-organized, maintainable code
✅ **SOLID Principles** - All 5 principles in action
✅ **Dependency Injection** - Flexible, testable design
✅ **Easy Testing** - No file I/O in tests thanks to DIP
✅ **Extensibility** - Add new features without breaking existing code

## 🔍 Code Structure

```
python/
├── task_manager/           # Main package
│   ├── task.py            # Task model (SRP)
│   ├── storage.py         # Storage layer (OCP, LSP, ISP, DIP)
│   ├── service.py         # Business logic (SRP, DIP)
│   ├── formatter.py       # Output formatting (SRP, ISP)
│   └── cli.py             # CLI interface (SRP, DIP)
├── task.py                # Entry point
├── demo.py                # Interactive demo
└── test_task_manager.py   # Test suite
```

## 🎯 Next Steps

1. ✅ Run the demo: `python demo.py`
2. ✅ Try the CLI: `python task.py add "Learn SOLID"`
3. ✅ Run tests: `python test_task_manager.py`
4. ✅ Read the code and comments
5. ✅ Study [SOLID_PRINCIPLES.md](./python/SOLID_PRINCIPLES.md)

## 💬 Key Takeaways

After exploring this project, you should understand:

- **Why** each SOLID principle matters
- **How** to apply them in real code
- **When** to use (and not use) each principle
- **Trade-offs** involved in good design

Happy learning! 🚀
