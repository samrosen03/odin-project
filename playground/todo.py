def show_menu():
    print("\nTodo App Menu:")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Delete Task")
    print("4. Exit")

def add_task(tasks):
    task = input("Enter a new task: ")
    tasks.append(task)
    print("Task added!")

def view_tasks(tasks):
    if not tasks:
        print("No tasks yet.")
    else:
        print("\nYour Tasks:")
        for idx, task in enumerate(tasks, 1):
            print(f"{idx}. {task}")

def delete_task(tasks):
    if not tasks:
        print("No tasks to delete.")
        return
    view_tasks(tasks)
    try:
        idx = int(input("Enter the task number to delete: "))
        if 1 <= idx <= len(tasks):
            removed = tasks.pop(idx - 1)
            print(f"Deleted: {removed}")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def main():
    tasks = []
    while True:
        show_menu()
        choice = input("Choose an option (1-4): ")
        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            delete_task(tasks)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()
