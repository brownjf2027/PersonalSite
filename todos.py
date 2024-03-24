import json


# Function to add a new item to the todo list
def add_item(title, description):
    with open('todo.json', 'r') as file:
        todo_list = json.load(file)

    new_item = {"title": title, "description": description}
    todo_list.append(new_item)

    with open('todo.json', 'w') as file:
        json.dump(todo_list, file, indent=4)


# Function to remove an item from the todo list by title
def remove_item(title):
    with open('todo.json', 'r') as file:
        todo_list = json.load(file)

    todo_list = [item for item in todo_list if item["title"] != title]

    with open('todo.json', 'w') as file:
        json.dump(todo_list, file, indent=4)
