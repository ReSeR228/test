import json
import os

TASKS_FILE = 'tasks.json'
PRIORITY = {"1": "низкий", "2": "средний", "3": "высокий"}
STATUS = {"1": "новая", "2": "в процессе", "3": "завершена"}

tasks = {}


def load_tasks():
    global tasks
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            tasks = json.load(file)


def save_tasks():
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)


def get_next_id():
    if tasks:
        return max(int(id) for id in tasks.keys()) + 1
    return 1


def create_task(title, description, priority, status):
    task_id = str(get_next_id())
    tasks[task_id] = {
        "title": title,
        "description": description,
        "priority": PRIORITY[priority],
        "status": STATUS[status]
    }
    save_tasks()


def update_task(task_id, field, value):
    if task_id in tasks:
        if field == 'priority':
            value = PRIORITY[value]
        elif field == 'status':
            value = STATUS[value]
        tasks[task_id][field] = value
        save_tasks()


def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        save_tasks()


def read_tasks():
    return tasks


load_tasks()


def main_menu():
    while True:
        print("\nВыберите действие:")
        print("1 - Создать новую задачу")
        print("2 - Просмотреть задачи")
        print("3 - Обновить задачу")
        print("4 - Удалить задачу")
        print("0 - Выйти из программы")

        choice = input("Введите номер действия: ")

        if choice == '1':
            create_task_menu()
        elif choice == '2':
            view_tasks_menu()
        elif choice == '3':
            update_task_menu()
        elif choice == '4':
            delete_task_menu()
        elif choice == '0':
            break
        else:
            print("Неверный ввод, попробуйте еще раз.")


def create_task_menu():
    title = input("Введите название задачи: ")
    description = input("Введите описание задачи: ")
    priority = input("Введите приоритет (1 - низкий, 2 - средний, 3 - высокий): ")
    while priority not in PRIORITY:
        print("Неверный ввод.")
        priority = input("Введите приоритет (1 - низкий, 2 - средний, 3 - высокий): ")

    status = input("Введите статус (1 - новая, 2 - в процессе, 3 - завершена): ")
    while status not in STATUS:
        print("Неверный ввод.")
        status = input("Введите статус (1 - новая, 2 - в процессе, 3 - завершена): ")

    create_task(title, description, priority, status)
    print("Задача создана.")


def view_tasks_menu():
    while True:
        print("\nПросмотр задач:")
        print("1 - Отобразить задачи в изначальном виде")
        print("2 - Отсортировать по статусу")
        print("3 - Отсортировать по приоритету")
        print("4 - Поиск по названию или описанию")
        print("0 - Вернуться в главное меню")

        choice = input("Введите номер действия: ")

        if choice == '1':
            display_tasks(tasks)
        elif choice == '2':
            sorted_tasks = sorted(tasks.items(), key=lambda x: x[1]['status'])
            display_tasks(dict(sorted_tasks))
        elif choice == '3':
            sorted_tasks = sorted(tasks.items(), key=lambda x: x[1]['priority'])
            display_tasks(dict(sorted_tasks))
        elif choice == '4':
            keyword = input("Введите ключевое слово для поиска: ").lower()
            search_tasks(keyword)
        elif choice == '0':
            break
        else:
            print("Неверный ввод, попробуйте еще раз.")


def display_tasks(tasks):
    for task_id, task in tasks.items():
        print(f"ID: {task_id}, Название: {task['title']}, Описание: {task['description']}, "
              f"Приоритет: {task['priority']}, Статус: {task['status']}")


def search_tasks(keyword):
    results = {task_id: task for task_id, task in tasks.items() if
               keyword in task['title'].lower() or keyword in task['description'].lower()}
    if results:
        display_tasks(results)
    else:
        print("Задачи не найдены.")


def update_task_menu():
    task_id = input("Введите ID задачи для обновления: ")
    if task_id in tasks:
        print("Что вы хотите обновить?")
        print("1 - Название")
        print("2 - Описание")
        print("3 - Приоритет")
        print("4 - Статус")

        field_choice = input("Введите номер поля: ")
        field_map = {'1': 'title', '2': 'description', '3': 'priority', '4': 'status'}

        if field_choice in field_map:
            field = field_map[field_choice]
            value = input(f"Введите новое значение для {field}: ")
            if field in ['priority', 'status']:
                while value not in (PRIORITY if field == 'priority' else STATUS):
                    print("Неверный ввод.")
                    value = input(f"Введите новое значение для {field}: ")
            update_task(task_id, field, value)
            print("Задача обновлена.")
        else:
            print("Неверный выбор поля.")
    else:
        print("Задача не найдена.")


def delete_task_menu():
    task_id = input("Введите ID задачи для удаления: ")
    if task_id in tasks:
        delete_task(task_id)
        print("Задача удалена.")
    else:
        print("Задача не найдена.")


if __name__ == "__main__":
    main_menu()