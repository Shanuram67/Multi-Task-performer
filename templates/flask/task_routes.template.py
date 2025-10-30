from flask import Blueprint, request, jsonify

task_bp = Blueprint('task', __name__)

# GET all tasks
@task_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    # TODO: Fetch tasks from database
    tasks = [
        {'id': 1, 'title': 'Sample Task', 'owner': 'admin'},
        {'id': 2, 'title': 'Another Task', 'owner': 'user'}
    ]
    return jsonify(tasks)

# POST new task
@task_bp.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    # TODO: Save new task to DB
    return jsonify({'message': 'Task created successfully', 'task': data}), 201

# PUT update task
@task_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    # TODO: Update task in DB
    return jsonify({'message': f'Task {task_id} updated', 'data': data})

# DELETE task
@task_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # TODO: Delete task from DB
    return jsonify({'message': f'Task {task_id} deleted'})
