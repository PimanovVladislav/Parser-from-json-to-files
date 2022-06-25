import os
from datetime import datetime
import requests


def create_new_file(username, str_report):
    filename = f'tasks/{username}.txt'
    # noinspection PyBroadException
    try:
        with open(filename, "w") as f:
            f.write(str_report)
    except Exception:
        print(f'Что-то пошло не так при работе с файлом "{filename}".')


def rename_old_file(username):
    filename = f'tasks/{username}.txt'
    # noinspection PyBroadException
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        pass
    except Exception:
        print(f'Что-то пошло не так при работе с файлом "{filename}".')
    else:
        date_created_old_file = file.readlines()[1][-17:-1]
        old_filename = f"tasks/old_{username}_{date_created_old_file[6:10]}-" \
                       f"{date_created_old_file[3:5]}-" \
                       f"{date_created_old_file[0:2]}T" \
                       f"{date_created_old_file[11:13]}-" \
                       f"{date_created_old_file[14:]}.txt"
        file.close()
        os.rename(filename, old_filename)


def create_lists_todos(todos, id_user):
    list_completed_todos = []
    list_not_completed_todos = []
    for todo in todos:
        if todo.get('userId', 0) == id_user:
            shortnames_todo = todo.get('title', 0)
            if len(shortnames_todo) > 48:
                shortnames_todo = f"{shortnames_todo[:48]}..."
            if todo.get('completed', 0):
                list_completed_todos.append(shortnames_todo)
            else:
                list_not_completed_todos.append(shortnames_todo)
    return list_completed_todos, list_not_completed_todos


def create_actually_files(users, todos):
    for user in users:
        username = user['username']
        name_company = user['company']['name']
        name = user['name']
        email_address = user['email']
        list_completed_todos, list_not_completed_todos = create_lists_todos(todos, user['id'])
        date_created = datetime.today().strftime("%d.%m.%Y %H:%M")
        separator = '\n'
        str_report = f'Отчет для {name_company}.\n' \
                     f'{name} <{email_address}> {date_created}\n' \
                     f'Всего задач: {len(list_completed_todos + list_not_completed_todos)}\n\n' \
                     f'Завершенные задачи ({len(list_completed_todos)}):\n' \
                     f'{separator.join(list_completed_todos)}\n\n' \
                     f'Оставшиеся задачи ({len(list_not_completed_todos)}):\n' \
                     f'{separator.join(list_not_completed_todos)}\n'
        rename_old_file(username)
        create_new_file(username, str_report)


if __name__ == '__main__':
    dir_name = 'tasks'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    try:
        response_users = requests.get("https://json.medrating.org/users").json()
        response_todos = requests.get("https://json.medrating.org/todos").json()
        create_actually_files(response_users, response_todos)
    except requests.exceptions.RequestException:
        print('Что-то пошло не так при обращении к сети.')
