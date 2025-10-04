# Project 1: Task Manager CLI

**Duration**: Weeks 1-2 (10-14 hours)  
**Focus**: SOLID Principles in Practice  
**Languages**: Python first, then TypeScript

---

## 🎯 Project Overview

Build a command-line task management application that demonstrates all 5 SOLID principles in action. This project will teach you proper class design, separation of concerns, and how to write extensible, maintainable code.

## 📋 Functional Requirements

### Core Features

1. **Add tasks** with title, description, priority (low/medium/high), and due date
2. **List tasks** with filtering options (by status, priority, date)
3. **Update tasks** (mark complete, change priority, edit details)
4. **Delete tasks**
5. **Persist data** to JSON file
6. **Search tasks** by keyword in title or description

### CLI Commands

```bash
# Add a task
task add "Write documentation" --description "Complete API docs" --priority high --due "2025-10-10"

# List all tasks
task list

# List with filters
task list --status pending
task list --priority high
task list --status completed

# Mark task as complete
task complete 1

# Update a task
task update 1 --priority medium --description "Updated description"

# Delete a task
task delete 1

# Search tasks
task search "documentation"

# Show statistics
task stats
```
