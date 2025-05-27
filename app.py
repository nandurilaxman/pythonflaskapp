from flask import Flask, request, jsonify

app = Flask(__name__)

todos = []
todo_id = 1

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos), 200

@app.route('/todos', methods=['POST'])
def add_todo():
    global todo_id
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({"error": "Task is required"}), 400
    todo = {"id": todo_id, "task": data['task'], "completed": False}
    todos.append(todo)
    todo_id += 1
    return jsonify(todo), 201

@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    for todo in todos:
        if todo['id'] == id:
            todo['task'] = data.get('task', todo['task'])
            todo['completed'] = data.get('completed', todo['completed'])
            return jsonify(todo), 200
    return jsonify({"error": "Todo not found"}), 404

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    global todos
    todos = [todo for todo in todos if todo['id'] != id]
    return jsonify({"message": "Todo deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
