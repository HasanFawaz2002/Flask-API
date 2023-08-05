import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from TaskModel import TasksModel
from TaskController import get_all_tasks, get_task_by_id, create_task, update_task, delete_task, delete_all_tasks  

import psycopg2
app = Flask(__name__)

db = SQLAlchemy(app)

Base = declarative_base()



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


    


@app.route('/task', methods=['GET'])
def get_tasks():
    return get_all_tasks(db)

@app.route('/task/<int:task_id>', methods=['GET'])
def get_single_task(task_id):
    return get_task_by_id(db, task_id)



@app.route('/task', methods=['POST'])
def post_task():
    try:
        data = request.json
        if not data or 'title' not in data or 'description' not in data or 'completed' not in data:
            return jsonify({'message': 'Missing required data'}), 400
        title = data['title']
        description = data['description']
        completed = data['completed']
        return create_task(db, title, description, completed)  
    except Exception as e:
        return jsonify({'message': 'Error processing request', 'error': str(e)}), 500
    

@app.route('/task/<int:task_id>', methods=['PUT'])
def put_task(task_id):
    try:
        data = request.json
        return update_task(db, task_id, data)  
    except Exception as e:
        return jsonify({'message': 'Error processing request', 'error': str(e)}), 500

@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_single_task(task_id):
    return delete_task(db, task_id) 


@app.route('/task', methods=['DELETE'])
def delete_all_tasks_route():
    return delete_all_tasks(db)

session.close()

if __name__ == '__main__':
    app.run(debug=True)