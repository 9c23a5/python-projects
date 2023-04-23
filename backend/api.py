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


from flask import Flask, jsonify, request, abort, make_response
from json import loads

class Todo:
    def __init__(self, id:int, title:str, completed:bool):
        self.id = id
        self.title = title
        self.completed = completed
        self.deleted = False

    def to_dict(self):
        return {"id":self.id, "title":self.title, "completed":self.completed}

    def delete(self):
        self.deleted = True
    
    def complete(self):
        self.completed = True

    def uncomplete(self):
        self.completed = False

    def rename(self, new_title):
        self.title = new_title

class TodoList:
    def __init__(self):
        # TodoList is a list of Todo
        self.list = []

    def get_next_id(self):
        # We start with ID 1, and we dont remove deleted Todos
        # so we are safe to only +1 list length
        return len(self.list)+1

    def add(self, title, completed=False):
        new_todo = Todo(self.get_next_id(), title, completed)
        self.list.append(new_todo)
        return new_todo

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
        return iter([todo for todo in self.list if not todo.deleted])


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

todos = TodoList()
todos.add("test1")
todos.add("test2", True)
todos[2].delete()

@app.route("/todos")
# GET /todos: Returns a list of all todos.
def get_todos():
    return jsonify([task.to_dict() for task in todos])

@app.route("/todos", methods=["POST"])
# POST /todos: Creates a new todo
def create_todo():
    data = request.json
    try:
        new_todo = todos.add(data['title'], data['completed'])
        return jsonify(new_todo.to_dict())
    except:
        return invalid_req()


@app.errorhandler(400)
def invalid_req():
    return make_response(jsonify(error=True, status=400, message="Request malformed"), 400)

@app.errorhandler(404)
def not_found():
    return make_response(jsonify(error=True, status=404, message="Todo not found"), 404)


if __name__ == "__main__":
    app.run()
