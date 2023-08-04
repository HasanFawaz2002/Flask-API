import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
app = Flask(__name__)

db = SQLAlchemy(app)

Base = declarative_base()

class TasksModel(db.Model):
    __tablename__ = 'tasks' 
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    completed = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title}, description={self.description}, completed={self.completed})"
    
    @classmethod
    def create_table(cls, engine):
        Base.metadata.create_all(engine)

url = "postgresql://postgres:hasan@localhost/userTaskManagement"


def get_engine():
    try:
        if url is None:
            raise ValueError("DATABASE_URL environment variable is not set")
        
        if not database_exists(url):
            create_database(url)
        
        engine = create_engine(url, pool_size=50, echo=False)
        return engine
    except Exception as e:
        print(f"Error getting engine: {e}")
        return None

engine = get_engine()

if engine is not None:
    print("Engine created successfully.")
    print(f"Database URL: {engine.url}")
else:
    print("Engine creation failed.")




app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:hasan@localhost/userTaskManagement"
connection = psycopg2.connect(url) 



Session = sessionmaker(bind=engine)
session = Session()
TasksModel.create_table(engine)
session.commit()

def serialize_task(task):
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description, 
        'completed': task.completed
    }
    


@app.route('/task', methods=['GET'])
def get_all_tasks():
    tasks = db.session.query(TasksModel).all()
    
    if not tasks:
        return jsonify({'message': 'No tasks found'}), 404
    
    tasks_list = [serialize_task(task) for task in tasks]
    return jsonify(tasks_list)

@app.route('/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = session.query(TasksModel).get(task_id)  

    if not task:
        return jsonify({'message': 'Task not found'}), 404
    
    task_dict = serialize_task(task)
    return jsonify(task_dict)



@app.route('/task', methods=['POST'])
def create_task():
    try:
        data = request.json
        if not data or 'title' not in data or 'description' not in data or 'completed' not in data:
            return jsonify({'message': 'Missing required data'}), 400
        task = TasksModel(title=data['title'], description=data['description'], completed=data['completed'])
        db.session.add(task)
        db.session.commit()
        task_dict = serialize_task(task)
        return jsonify(task_dict), 201
    except Exception as e:
        return jsonify({'message': 'Error processing request', 'error': str(e)}), 500
    

@app.route('/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = TasksModel.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    
    data = request.json
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = data['completed']
    
    try:
        db.session.commit() 
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
    
    task_dict = serialize_task(task)
    return jsonify(task_dict)

@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = TasksModel.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task Deleted'}), 204

session.close()

if __name__ == '__main__':
    app.run(debug=True)
