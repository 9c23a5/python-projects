# Write a program that implements a simple RESTful API for a todo list. The API should have the following endpoints:
# 
# GET /todos: Returns a list of all todos.
# POST /todos: Creates a new todo.
# GET /todos/<id>: Returns the todo with the specified ID.
# PUT /todos/<id>: Updates the todo with the specified ID.
# DELETE /todos/<id>: Deletes the todo with the specified ID.
# 
# Each todo should have the following properties:
# id: A unique identifier for the todo.
# title: A short title describing the todo.
# completed: A boolean indicating whether the todo has been completed.
# 
# The API should store the todo data in memory, without using a database.
# You can use the Flask web framework to implement the API, and the JSON module to serialize and deserialize JSON data.


from flask import Flask

class Todo:
    def __init__(self, id, title, completed):
        self.id = id
        self.title = title
        self.completed = completed
        self.deleted = False


class TodoList:
    def __init__(self):
        self.list = []

    def get_next_id(self):
        return len(self.list)+1

    def add(self, title, completed=False):
        new_todo = Todo(self.get_next_id(), title, completed)
        self.list.append(new_todo)

    def rename(self, id, new_title):
        self[id].title = new_title

    def complete(self, id):
        self[id].completed = True

    def uncomplete(self, id):
        self[id].completed = False

    def delete(self, id):
        self[id].deleted = True

    def __getitem__(self, id):
        # We start with ID 1, so -1 to this
        try:
            todo = self.list[id-1]
            if not todo.deleted:
                return todo
            else:
                abort(404)
        except IndexError:
            abort(404)

    def __iter__(self):
        return iter(self.list)

app = Flask(__name__)
todos = TodoList()
todos.add("test1")
todos.add("test2", True)

@app.route("/todos")
def get_todos():
    return_object = {}
    for task in todos:
        print(task.id,task.title,task.completed)
    return "im todos"

if __name__ == "__main__":
    app.run()

# Write a program that implements a simple RESTful API for a todo list. The API should have the following endpoints:
# 
# GET /todos: Returns a list of all todos.
# POST /todos: Creates a new todo.
# GET /todos/<id>: Returns the todo with the specified ID.
# PUT /todos/<id>: Updates the todo with the specified ID.
# DELETE /todos/<id>: Deletes the todo with the specified ID.
# 
# Each todo should have the following properties:
# id: A unique identifier for the todo.
# title: A short title describing the todo.
# completed: A boolean indicating whether the todo has been completed.
# 
# The API should store the todo data in memory, without using a database.
# You can use the Flask web framework to implement the API, and the JSON module to serialize and deserialize JSON data.


from flask import Flask

class Todo:
    def __init__(self, id, title, completed):
        self.id = id
        self.title = title
        self.completed = completed
        self.deleted = False


class TodoList:
    def __init__(self):
        self.list = []

    def get_next_id(self):
        return len(self.list)+1

    def add(self, title, completed=False):
        new_todo = Todo(self.get_next_id(), title, completed)
        self.list.append(new_todo)

    def rename(self, id, new_title):
        self[id].title = new_title

    def complete(self, id):
        self[id].completed = True

    def uncomplete(self, id):
        self[id].completed = False

    def delete(self, id):
        self[id].deleted = True

    def __getitem__(self, id):
        # We start with ID 1, so -1 to this
        try:
            todo = self.list[id-1]
            if not todo.deleted:
                return todo
            else:
                abort(404)
        except IndexError:
            abort(404)

    def __iter__(self):
        return iter(self.list)

app = Flask(__name__)
todos = TodoList()
todos.add("test1")
todos.add("test2", True)

@app.route("/todos")
def get_todos():
    return_object = {}
    for task in todos:
        print(task.id,task.title,task.completed)
    return "im todos"

if __name__ == "__main__":
    app.run()