from flask import jsonify
from TaskModel import TasksModel

def serialize_task(task):
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed,
        'task_category': task.task_category,  
        'task_priority': task.task_priority,  
        'due_date':task.due_date
    }
    
    

# GET All Tasks
def get_all_tasks(db):
    tasks = db.session.query(TasksModel).all()

    if not tasks:
        return jsonify({'message': 'No tasks found'}), 404

    tasks_list = [serialize_task(task) for task in tasks]
    return jsonify(tasks_list)

# GET Task by its ID
def get_task_by_id(db, task_id):
    task = db.session.query(TasksModel).get(task_id)

    if not task:
        return jsonify({'message': 'Task not found'}), 404

    task_dict = serialize_task(task)
    return jsonify(task_dict)


#Create task
def create_task(db, title, description, completed, task_category, task_priority,due_date):
    try:
        task = TasksModel(
            title=title,
            description=description,
            completed=completed,
            task_category=task_category,
            task_priority=task_priority,
            due_date=due_date
        )
        db.session.add(task)
        db.session.commit()
        task_dict = serialize_task(task)
        return task_dict, 201
    except Exception as e:
        return {'message': 'Error processing request', 'error': str(e)}, 500
    


#Update task
def update_task(db, task_id, data):
    task = db.session.query(TasksModel).get(task_id)

    if not task:
        return jsonify({'message': 'Task not found'}), 404

    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = data['completed']
    if 'task_category' in data:
        task.task_category = data['task_category']
    if 'task_priority' in data:
        task.task_priority = data['task_priority']
    if 'due_date' in data:
        task.due_date = data['due_date']
    try:
        db.session.commit()
        task_dict = serialize_task(task)
        return task_dict
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


#Delete Task
def delete_task(db, task_id):
    task = db.session.query(TasksModel).get(task_id)

    if not task:
        return jsonify({'message': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Task Deleted'}), 204


#Delete All Tasks
def delete_all_tasks(db):
    try:
        db.session.query(TasksModel).delete()
        db.session.commit()
        return jsonify({'message': 'All tasks deleted'}), 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting tasks', 'error': str(e)}), 500