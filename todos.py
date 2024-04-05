import json


# Function to add a new item to the todo list
def add_item(js_data):
    with open('static/files/todo.json', 'r') as file:
        todo_list = json.load(file)

    new_item = js_data
    todo_list.append(new_item)

    with open('static/files/todo.json', 'w') as file:
        json.dump(todo_list, file, indent=4)


# Function to remove an item from the todo list by title
def remove_item(title):
    with open('static/files/todo.json', 'r') as file:
        todo_list = json.load(file)

    todo_list = [item for item in todo_list if item["title"] != title]

    with open('static/files/todo.json', 'w') as file:
        json.dump(todo_list, file, indent=4)

