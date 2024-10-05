import json

PRIORITIES = {"1": "low", "2": "medium", "3": "high"}
STATUSES = {"1": "new", "2": "in progress", "3": "completed"}
TASKS_FILE = 'kinda_db.txt'


def pull_data_from_db() -> dict[str] or dict[None]:
    try:
        with open(TASKS_FILE, 'r') as file:
            tasks = json.load(file)
            return tasks
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Error reading tasks. File may be corrupted")
        return {}


def push_data_back_to_db(tasks: dict):
    with open(TASKS_FILE, "w") as file:
       file.write(json.dumps(tasks, indent=4))


def get_next_id(tasks: dict) -> int:
    """
        Get next id in order to return completed dict from (create_task) function,
        where ID is a key and value(type(dict)) is a task info.
    """
    if tasks:
        ids_list = list(map(lambda i: int(i), tasks.keys()))
        ids_list.sort()
        return ids_list[-1] + 1
    else:
        return 1


def create_task(tasks):
    task_id = str(get_next_id(tasks))
    title = input("Enter Task Title: ")
    description = input("Enter Task Description: ")

    while True:
        priority = input("Select Priority (1 - low, 2 - medium, 3 - high): ")
        if priority in PRIORITIES:
            break
        print("Invalid input. Please try again.")

    while True:
        status = input("Select Status (1 - new, 2 - in progress, 3 - completed): ")
        if status in STATUSES:
            break
        print("Invalid input. Please try again.")

    push_data_back_to_db(add_task_info_into_task_list(
        tasks,
        title=title,
        description=description,
        priority=PRIORITIES[priority],
        status=STATUSES[status]
    ))

    print(f"Task {task_id} Created Successfully")


def add_task_info_into_task_list(tasks: dict[str], **kwargs: str) -> dict[str]:
    task_id = get_next_id(tasks)
    tasks.update({task_id: kwargs})
    return tasks


def view_tasks_list(tasks: dict[str], optional_sort: str = None):
    """
    :param tasks: added this comment in order to bypass warning:)
    :param optional_sort: is the key by which the sorting is performed, if needed.
    """
    if optional_sort:
        tasks = dict(sorted(tasks.items(), key=lambda item: item[1][optional_sort]))

    for key, value in tasks.items():
        print(
            f"ID: {key} - Title: {value['title']},"
            f" Description: {value['description']},"
            f" Priority: {value['priority']},"
            f" Status: {value['status']}")


def search_for_task(tasks: dict[str]):
    keyword = input("Enter Keyword for search: ").lower()
    found_tasks = {task_id: task for task_id, task in tasks.items() if keyword in task['title'].lower()
                   or keyword in task['description'].lower()}
    if found_tasks:
        view_tasks_list(found_tasks)
    else:
        print("Task not Found")


def delete_task(tasks: dict[str]):
    task_id = ""
    try:
        task_id = input("Enter task id you want to remove: ")
        if task_id in tasks:
            del tasks[task_id]
            push_data_back_to_db(tasks)
            print(f"Task {task_id} was deleted successfully")
        else:
            print("Task not found")
    except KeyError:
        print(f"Task {task_id} does not exist")


def update_task(tasks: dict[str]) -> dict[str] or None:
    task_id = input("Enter the task ID to update: ")
    if task_id not in tasks:
        print("Task not found")
        return

    print("What would you like to update?")
    print("1 - Name")
    print("2 - Description")
    print("3 - Priority")
    print("4 - Status")

    users_choice = input("Enter your choice: ")

    if users_choice == '1':
        tasks[task_id]['name'] = input("Enter the new name: ")
    elif users_choice == '2':
        tasks[task_id]['description'] = input("Enter the new description: ")
    elif users_choice == '3':
        while True:
            priority = input("Choose a priority (1 - low, 2 - medium, 3 - high): ")
            if priority in PRIORITIES:
                tasks[task_id]['priority'] = PRIORITIES[priority]
                break
            print("Invalid input. Please try again")
    elif users_choice == '4':
        while True:
            status = input("Choose a status (1 - new, 2 - in progress, 3 - completed): ")
            if status in STATUSES:
                tasks[task_id]['status'] = STATUSES[status]
                break
            print("Invalid input. Please try again")

    push_data_back_to_db(tasks)
    print(f"Task {task_id} has been updated")


def display_menu():
    """Displays the main menu for task management options"""
    print("Task Management System")
    print("1 - Create a new task")
    print("2 - View tasks")
    print("3 - Update a task")
    print("4 - Delete a task")
    print("5 - Search for a task")
    print("0 - Exit")


def main():
    """
        Main function to run the "Shity" task management system
        Provides a menu for users to create, view, update, and delete tasks.
        Tasks are saved to and loaded from a text file, allowing for storage
        The End!:)
    """

    tasks = pull_data_from_db()
    while True:
        display_menu()
        user_choice = input("Select Any Option: ")

        match user_choice:
            case "1":
                create_task(tasks)
            case "2":
                print("1 - Display tasks in their original form")
                print("2 - Sort by Status")
                print("3 - Sort by Priority")
                print("4 - Search by title or Description")
                user_view_choice = input("So Your Choice....: ")
                if user_view_choice == "1":
                    view_tasks_list(tasks)
                elif user_view_choice == "2":
                    view_tasks_list(tasks, 'status')
                elif user_view_choice == "3":
                    view_tasks_list(tasks, 'priority')
                elif user_view_choice == "4":
                    search_for_task(tasks)
            case "3":
                update_task(tasks)
            case "4":
                delete_task(tasks)
            case "5":
                search_for_task(tasks)
            case "0":
                break
            case _:
                print("Invalid input. Please try again.")


if __name__ == '__main__':
    main()
