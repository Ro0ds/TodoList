# imports
from datetime import date
from enum import Enum, IntEnum
import json
import os
import random as rd

# global variables
name = ''
JSON_FILE = ''
task_list = []
brute_json = []
task = {}
isFileSaved = False

# enum
class Priority(IntEnum):
    normal = 1,
    important = 2,
    urgent = 3

# functions / methods
def create_user_file(user_name):
    global JSON_FILE
    
    if not os.path.isfile(JSON_FILE):    
        file = open(JSON_FILE, 'x')
        file.close()
    
    create_sample_task()

def store_data(user_data):
    global JSON_FILE
    create_user_file()

    if len(user_data) > 0: # if there is user data
        with open(JSON_FILE, 'w') as file:
            file.write(user_data)

def menu():
    op = input(f'\nWelcome to {name} Task Manager!\n' +
          f'Choose from the options below\n' +
          f'1 - Create new task\n' +
          f'2 - Show tasks\n' +
          f'3 - Show task by id\n' +
          f'4 - Edit task by id\n' +
          f'5 - Delete task by id\n' +
          f'0 - Exit\n'
          ' > '
        )
    return op

def create_sample_task():
    task = {
        'hash': 1,
        'Task name': 'sample task',
        'Created': '01/01/1900',
        'Finish': '01/01/9999',
        'Priotiry': 'normal'
    }

    task_list.append(task)
    save_to_file(task_list)

def create_task():
    print('\n>> Creating task...')
    _hash = rd.randint(1, 300)
    _task_name = input('Task name > ')
    _created = date.today().strftime('%d/%m/%Y')
    _finish = input('End date (dd/MM/yyyy) > ')
    _priority = int(input('Priority\n' +
                     f'1 - {Priority.normal.name}\n' +
                     f'2 - {Priority.important.name}\n' +
                     f'3 - {Priority.urgent.name}\n' +
                     '> '
                        )
                    )

    task = {
        "hash": _hash,
        "Task name": _task_name,
        "Created": _created,
        "Finish": _finish,
        "Priority": Priority(_priority).name
        }

    task_list = brute_json

    task_list.append(task)
    save_to_file(task_list)

def show_tasks():
    user_json = json.dumps(brute_json, indent=4, separators=(',', ' = '))
    return user_json
    
def show_task(id):
    for user_task in brute_json:
        if user_task['hash'] == id:
            return json.dumps(user_task, indent=4, separators=(',', ' = '))

def edit_task(id):
    for user_task in brute_json:
        if user_task['hash'] == id:
            _original = json.dumps(user_task, indent=4, separators=(',', ' = '))
            print(f'\nOriginal task: {_original}\n')

            _hash = user_task['hash']
            _created = user_task['Created']
            
            if input('Change task name? (Y/N) > ').upper() == 'Y':
                _task_name = input('New task name > ')
            else:
                _task_name = user_task['Task name']
            if input('Change finish date? (Y/N) > ').upper() == 'Y':
                _finish = input('New finish date (dd/MM/yyyy) > ')
            else:
                _finish = user_task['Finish']
            if input('Change priority? (Y/N) > ').upper() == 'Y':
                _priority = int(input('New priority\n' +
                     f'1 - {Priority.normal.name}\n' +
                     f'2 - {Priority.important.name}\n' +
                     f'3 - {Priority.urgent.name}\n' +
                     '> ')
                     )
            else:
                _priority = user_task['Priority']

            user_task = {
                "hash": _hash,
                "Task name": _task_name,
                "Created": _created,
                "Finish": _finish,
                "Priority": Priority(_priority).name
            }
    
            updated_task_list = delete_task(id)
            updated_task_list.append(user_task)

            save_to_file(updated_task_list)

            return json.dumps(user_task, indent=4, separators=(',', ' = '))

def delete_task(id):
    new_brute_json = [i for i in brute_json if not (i['hash'] == id)]

    return new_brute_json

def get_JSON_file_info():
    with open(JSON_FILE, encoding='utf-8', mode='r') as openfile:
        return json.load(openfile)
        
def get_JSON_id_list():
    keys_list = []
    for item in brute_json:
        keys_list.append(item['hash'])
        keys_list.sort()
    return keys_list

def save_to_file(json_item):
    with open(JSON_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(json_item, json_file, indent=4, separators=(',', ': '))
        print('>> Saved to file!')

# main program
name = input('Type your name \n> ')

JSON_FILE = os.path.join(os.getcwd(), f'{name.lower()}_data.json')

while True:
    if not os.path.isfile(JSON_FILE):
        option = input(f'Welcome {name}, do you want to store your tasks? (Y/N) \n> ')

        if option.upper() not in ('Y', 'N'):
            print('>> Wrong option, try again...')
            continue
        elif option.upper() == 'Y':
            print('>> Tasks will be stored and will stay available after closing the program')
            create_user_file(name)
        else:
            print(">> Tasks won't be stored and will only be available during this session.")
    
    brute_json = get_JSON_file_info()

    try:
        menu_option = int(menu())

        if menu_option not in (0, 1, 2, 3, 4, 5):
            print('>> Not a valid option, try again...')
            continue
        elif menu_option == 1:
            create_task()
        elif menu_option == 2:
            input(show_tasks() + '\npress any key to continue...')
        elif menu_option == 3:
            print(f"Task ID's list: {get_JSON_id_list()}")
            id = int(input('Type the task ID > '))
            input(show_task(id) + '\npress any key to continue...')
        elif menu_option == 4:
            print(f"Task ID's list: {get_JSON_id_list()}")
            id = int(input('Type the task ID > '))
            input(edit_task(id) + '\npress any key to continue...')
        elif menu_option == 5:
            print(f"Task ID's list: {get_JSON_id_list()}")
            id = int(input('Type the task ID > '))
            
            updated_task_list = delete_task(id)
            save_to_file(updated_task_list)
        elif menu_option == 0:
            break
    except:
        print('>> Not a valid option, try again...')
        continue
