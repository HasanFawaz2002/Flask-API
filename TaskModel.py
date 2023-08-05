from flask import Flask, request, jsonify
from sqlalchemy import  Column, Integer, String, Boolean,Enum,Date
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

db = SQLAlchemy(app)

Base = declarative_base()



class TasksModel(Base):
    __tablename__ = 'tasks' 
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    completed = Column(Boolean, nullable=False)
    task_category = Column(Enum('frontend', 'backend', name='task_categories'), nullable=False)
    task_priority = Column(Enum('important', 'not important', 'very important', name='task_priorities'), nullable=False)
    due_date = Column(Date, nullable=True)

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title}, description={self.description}, completed={self.completed}, task_category={self.task_category}, task_priority={self.task_priority}, due_date={self.due_date})"
    
    @classmethod
    def create_table(cls, engine):
        Base.metadata.create_all(engine)