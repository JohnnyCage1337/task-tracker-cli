# Task Tracker CLI
A simple command-line interface (CLI) to manage your to-do list. This application allows you to track tasks, their statuses, and modification history, storing all data locally in a JSON file.

## Features
- **Full CRUD Support**: Add, update, and delete tasks from the terminal.

- **Status Management**: Mark tasks as todo, in-progress, or done.

- **Filtering**: List all tasks or filter them by their current status.

- **Automatic Timestamps**: Every task tracks its creation time and last update time (accurate to the second).

- **No External Dependencies**: Built entirely using the Python Standard Library.

## Requirements
- Python 3.10+ (Required for structural pattern matching / match-case syntax).

## Installation
1. Clone this repository:

```Bash
git clone https://github.com/JohnnyCage1337/task-tracker-cli
cd task-tracker-cli
```
No additional installation is required.

## Usage
The application uses positional arguments to handle commands.

```Bash
# Adding a new task
python task_cli.py add "Buy groceries"

# Updating a task description
python task_cli.py update 1 "Buy groceries and cook dinner"

# Deleting a task
python task_cli.py delete 1

# Marking statuses
python task_cli.py mark-in-progress 1
python task_cli.py mark-done 1

# Listing tasks
python task_cli.py list              # Show all tasks
python task_cli.py list done         # Show only completed tasks
python task_cli.py list in-progress  # Show tasks currently being worked on
```
## Project Structure
- **task.py**: The core Task model and TaskStatus Enum. Handles data validation and time formatting.

- **task_manager.py**: Handles the business logic and file I/O (reading/writing to tasks.json).

- **task_cli.py**: The entry point of the application. Parses command-line arguments and displays output.

- **tests_task.py**: Unit tests for the Task class.

## Testing
To ensure data integrity and proper timestamping, run the included unit tests:

```Bash
python tests_task.py
```
## Data Storage
Tasks are stored in a tasks.json file in the root directory. If the file does not exist, the application will create it automatically upon the first run.

Each task entry follows this structure:

```JSON
{
    "id": 1,
    "description": "Buy groceries",
    "status": "todo",
    "createdAt": "2026-05-11 14:00:00",
    "updatedAt": "2026-05-11 14:00:00"
}
```