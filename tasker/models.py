from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from tasker import db, app

class Task(db.Model):
    # Your database model for persistence
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=True)
    assigned_to = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default='pending')
    user_id = db.Column(db.Integer, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    
    def change_status(self, new_status):
        # Validate status
        valid_statuses = ['pending', 'done', 'done_improperly'] # tasks can be rated
        if new_status not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")
        
        self.status = new_status
        print(f"Task {self.id} status changed to {self.status}")
    
    def edit(self, new_title, new_desc):
        self.title = new_title
        self.desc = new_desc
        self.change_status('pending')  # status reset while finishing edit
        print(f"Task {self.id} edited")

   
class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.tasks = []  # List to store assigned tasks
    
    def add_task(self, task):
        self.tasks.append(task)
        print(f"Task {task.id} assigned to {self.name}")


with app.app_context():
        db.create_all()