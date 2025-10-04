"""
CLI Interface - Demonstrates SRP and DIP

SRP: This class is responsible ONLY for CLI interaction (parsing args, displaying output).
     It doesn't handle business logic or storage.
DIP: Depends on abstractions (IStorage, ITaskFormatter) injected via constructor.
"""
import argparse
import sys
from task_manager.task import Task
from task_manager.service import TaskService
from task_manager.formatter import ITaskFormatter, SimpleFormatter, DetailedFormatter, StatisticsFormatter
from task_manager.storage import IStorage


class TaskCLI:
    """
    Command-line interface for task management.
    
    SRP: Responsible ONLY for CLI interaction.
    DIP: Depends on injected TaskService and formatters.
    """
    
    def __init__(self, service: TaskService, formatter: ITaskFormatter = None):
        """
        Initialize CLI with dependencies.
        
        DIP: Dependencies are injected, not created internally.
        """
        self.service = service
        self.formatter = formatter or SimpleFormatter()
        self.stats_formatter = StatisticsFormatter()
    
    def run(self, args: list = None):
        """
        Main entry point for CLI.
        
        Args:
            args: Command-line arguments (defaults to sys.argv[1:])
        """
        parser = self._create_parser()
        parsed_args = parser.parse_args(args if args is not None else sys.argv[1:])
        
        if not hasattr(parsed_args, 'func'):
            parser.print_help()
            return
        
        # Execute the appropriate command
        parsed_args.func(parsed_args)
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser with all subcommands."""
        parser = argparse.ArgumentParser(
            prog='task',
            description='Task Manager CLI - Demonstrating SOLID Principles'
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Add command
        add_parser = subparsers.add_parser('add', help='Add a new task')
        add_parser.add_argument('title', help='Task title')
        add_parser.add_argument('--description', '-d', default='', help='Task description')
        add_parser.add_argument('--priority', '-p', choices=['low', 'medium', 'high'],
                               default='medium', help='Task priority')
        add_parser.add_argument('--due', help='Due date (YYYY-MM-DD)')
        add_parser.set_defaults(func=self._add_task)
        
        # List command
        list_parser = subparsers.add_parser('list', help='List tasks')
        list_parser.add_argument('--status', choices=['pending', 'completed'],
                                help='Filter by status')
        list_parser.add_argument('--priority', choices=['low', 'medium', 'high'],
                                help='Filter by priority')
        list_parser.add_argument('--detailed', '-v', action='store_true',
                                help='Show detailed information')
        list_parser.set_defaults(func=self._list_tasks)
        
        # Complete command
        complete_parser = subparsers.add_parser('complete', help='Mark task as complete')
        complete_parser.add_argument('index', type=int, help='Task index')
        complete_parser.set_defaults(func=self._complete_task)
        
        # Update command
        update_parser = subparsers.add_parser('update', help='Update a task')
        update_parser.add_argument('index', type=int, help='Task index')
        update_parser.add_argument('--title', help='New title')
        update_parser.add_argument('--description', '-d', help='New description')
        update_parser.add_argument('--priority', '-p', choices=['low', 'medium', 'high'],
                                   help='New priority')
        update_parser.add_argument('--due', help='New due date (YYYY-MM-DD)')
        update_parser.set_defaults(func=self._update_task)
        
        # Delete command
        delete_parser = subparsers.add_parser('delete', help='Delete a task')
        delete_parser.add_argument('index', type=int, help='Task index')
        delete_parser.set_defaults(func=self._delete_task)
        
        # Search command
        search_parser = subparsers.add_parser('search', help='Search tasks')
        search_parser.add_argument('keyword', help='Search keyword')
        search_parser.set_defaults(func=self._search_tasks)
        
        # Stats command
        stats_parser = subparsers.add_parser('stats', help='Show statistics')
        stats_parser.set_defaults(func=self._show_stats)
        
        return parser
    
    def _add_task(self, args):
        """Add a new task."""
        try:
            task = Task(
                title=args.title,
                description=args.description,
                priority=args.priority,
                due_date=args.due
            )
            self.service.add_task(task)
            print(f"✓ Task added successfully: {task.title}")
        except Exception as e:
            print(f"✗ Error adding task: {e}", file=sys.stderr)
            sys.exit(1)
    
    def _list_tasks(self, args):
        """List tasks with optional filters."""
        try:
            tasks = self.service.get_all_tasks()
            
            # Apply filters
            if args.status:
                completed = args.status == 'completed'
                tasks = [t for t in tasks if t.completed == completed]
            
            if args.priority:
                tasks = [t for t in tasks if t.priority == args.priority]
            
            # Choose formatter
            if args.detailed:
                formatter = DetailedFormatter()
            else:
                formatter = self.formatter
            
            print(formatter.format_tasks(tasks))
        except Exception as e:
            print(f"✗ Error listing tasks: {e}", file=sys.stderr)
            sys.exit(1)
    
    def _complete_task(self, args):
        """Mark a task as complete."""
        try:
            if self.service.complete_task_by_index(args.index):
                print(f"✓ Task {args.index} marked as completed")
            else:
                print(f"✗ Task {args.index} not found", file=sys.stderr)
                sys.exit(1)
        except Exception as e:
            print(f"✗ Error completing task: {e}", file=sys.stderr)
            sys.exit(1)
    
    def _update_task(self, args):
        """Update task details."""
        try:
            task = self.service.get_task_by_index(args.index)
            if not task:
                print(f"✗ Task {args.index} not found", file=sys.stderr)
                sys.exit(1)
            
            updates = {}
            if args.title:
                updates['title'] = args.title
            if args.description:
                updates['description'] = args.description
            if args.priority:
                updates['priority'] = args.priority
            if args.due:
                updates['due_date'] = args.due
            
            if not updates:
                print("✗ No updates specified", file=sys.stderr)
                sys.exit(1)
            
            if self.service.update_task(task.id, **updates):
                print(f"✓ Task {args.index} updated successfully")
            else:
                print(f"✗ Failed to update task {args.index}", file=sys.stderr)
                sys.exit(1)
        except Exception as e:
            print(f"✗ Error updating task: {e}", file=sys.stderr)
            sys.exit(1)
    
    def _delete_task(self, args):
        """Delete a task."""
        try:
            if self.service.delete_task_by_index(args.index):
                print(f"✓ Task {args.index} deleted")
            else:
                print(f"✗ Task {args.index} not found", file=sys.stderr)
                sys.exit(1)
        except Exception as e:
            print(f"✗ Error deleting task: {e}", file=sys.stderr)
            sys.exit(1)
    
    def _search_tasks(self, args):
        """Search tasks by keyword."""
        try:
            tasks = self.service.search_tasks(args.keyword)
            if tasks:
                print(f"Found {len(tasks)} task(s) matching '{args.keyword}':\n")
                print(self.formatter.format_tasks(tasks))
            else:
                print(f"No tasks found matching '{args.keyword}'")
        except Exception as e:
            print(f"✗ Error searching tasks: {e}", file=sys.stderr)
            sys.exit(1)
    
    def _show_stats(self, args):
        """Show task statistics."""
        try:
            stats = self.service.get_statistics()
            print(self.stats_formatter.format_statistics(stats))
        except Exception as e:
            print(f"✗ Error getting statistics: {e}", file=sys.stderr)
            sys.exit(1)
