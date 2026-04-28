from tasker import app, db
from flask import request, redirect , render_template, url_for, flash
from tasker.models import Task, User
from tasker.forms import RegisterForm, LoginForm
from tasker import db
from flask_login import login_user, logout_user, login_required

@app.route('/', methods=['POST', 'GET'])
@login_required
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
  
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create=User(username=form.username.data, 
                            password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('index'))
    if form.errors != {}:
        for e in form.errors.values():
            flash(f'there was an error with creating a user: {e}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
            ):
                login_user(attempted_user)
                flash(f'Login successful! Logged in as: {attempted_user.username}', category='success')
                return redirect(url_for('index'))
        else:
            flash('Username and password are not matched! Please try again :)', category='danger')

    return render_template('login.html', form=form)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


@app.route('/logout')
@login_required
def logout_page():
    logout_user
    flash('You have been logged out!', category='info')
    return redirect(url_for('index'))



@app.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Task.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    
    except:
        return 'There was a problem with deleting the task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
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
@login_required
def mark_done(id):
    task = Task.query.get_or_404(id)
    task.status = 'done'
    
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem marking the task as done'

@app.route('/mark_improperly/<int:id>')
@login_required
def mark_improperly(id):
    task = Task.query.get_or_404(id)
    task.status = 'done improperly'
    
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem marking the task'