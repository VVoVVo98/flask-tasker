from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from tasker import db, app
from tasker import bcrypt

class Task(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=True)
    assigned_to = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default='pending')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Task %r>' % self.id
    
    def change_status(self, new_status):
        valid_statuses = ['pending', 'done', 'done improperly']
        if new_status not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")
        
        self.status = new_status
        print(f"Task {self.id} status changed to {self.status}")
    
    def edit(self, new_title, new_desc):
        self.title = new_title
        self.desc = new_desc
        self.change_status('pending')
        print(f"Task {self.id} edited")

   
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=30), nullable=False)
    tasks = db.relationship('Task', backref='tasked_user', lazy=True)

    @property
    def password(self):
         return self.password
    
    @password.setter
    def password(self, plain_text_password):
         self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
   
    
    def add_task(self, task):
        self.tasks.append(task)
        print(f"Task {task.id} assigned to {self.name}")

with app.app_context():
        db.create_all()