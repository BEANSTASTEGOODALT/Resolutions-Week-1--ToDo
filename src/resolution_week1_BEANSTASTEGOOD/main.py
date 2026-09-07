import argparse
import sys
import os
import json

TASKS_FILE = "tasks.json"

def load():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", help="List all tasks", action="store_true")
    parser.add_argument("-c", "--complete", type=int, help="Mark a task as complete by ID")
    parser.add_argument("-d", "--delete", type=int, help="Delete a task by ID")
    parser.add_argument("-e", "--edit", type=int, help="Edit a task by ID")
    parser.add_argument("-v", "--version", action="version", version="1.0", help="Show the version of the program")
    parser.add_argument("task", type=str, nargs="?", help="Task to add")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.list:
        tasks = load()
        if not tasks:
            print("No tasks!")
            sys.exit(0)
        for task in tasks:
            status = "x" if task["done"] else " "
            print(f"[{status}] {task['id']}: {task['task']}")
        sys.exit(0)
    elif args.complete:
        tasks = load()
        for task in tasks:
            if task["id"] == args.complete:
                task["done"] = True
                save(tasks)
                print(f"Task {args.complete} marked as complete")
                break
    elif args.delete:
        tasks = load()
        tasks = [task for task in tasks if task["id"] != args.delete]
        save(tasks)
        print(f"Task {args.delete} deleted")
    elif args.edit:
        tasks = load()
        for task in tasks:
            if task["id"] == args.edit:
                new_task = input("Enter the updated task description: ")
                task["task"] = new_task
                save(tasks)
                print(f"Task {args.edit} updated")
                break
    elif args.task:
        tasks = load()
        if len(tasks) == 0:
            new = 1
        else:
            new = tasks[-1]["id"] + 1
        tasks.append({"id": new, "task": args.task, "done": False})
        save(tasks)

        print(f"Task {args.task} added with ID of {new}")
        
if __name__ == "__main__":
    main()