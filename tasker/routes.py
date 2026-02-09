from tasker import app, db
from flask import request, redirect , render_template
from tasker.models import Task
from tasker.forms import RegisterForm

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form.get('desc', '')
        assigned_to = request.form.get('assigned_to', '')
   
        # Save to database
        new_task_db = Task(title=title, desc=desc, assigned_to=assigned_to, user_id=1)
        
        try:
            db.session.add(new_task_db)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue processing your form"

    else:
        tasks = Task.query.order_by(Task.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    
    except:
        return 'There was a problem with deleting the task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Task.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.title = request.form['title']
        task_to_update.desc = request.form.get('desc', '')
        task_to_update.assigned_to = request.form.get('assigned_to', '')

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue updating the task'

    else:
        return render_template('update.html', task=task_to_update)
    


@app.route('/mark_done/<int:id>')
def mark_done(id):
    task = Task.query.get_or_404(id)
    task.status = 'done'
    
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem marking the task as done'


@app.route('/mark_improperly/<int:id>')
def mark_improperly(id):
    task = Task.query.get_or_404(id)
    task.status = 'done_improperly'
    
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem marking the task'
    
@app.route('/register')
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)