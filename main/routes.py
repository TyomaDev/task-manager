from datetime import datetime

from flask import render_template, url_for, flash, redirect, request, abort
from main import app, db, bcrypt
from main.forms import RegistrationForm, LoginForm, TaskForm
from main.models import User, Task
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def landing():
    return render_template('landing.html', title='Simple Manager')

@login_required
@app.route("/task", methods=['GET', 'POST'])
def task():
    form = TaskForm()
    if request.args.get('change') :
        task = Task.query.get_or_404(int(request.args.get('change')))
        if task.author_id != current_user.id:
            abort(403)
        form.title.data = task.title
        form.description.data = task.description
        if form.validate_on_submit():
            form = TaskForm()
            task.title = form.title.data
            task.description = form.description.data
            task.date = datetime.now()
            db.session.commit()
            flash('Задача изменена', 'success')
            return redirect(request.path, code=302)
    elif request.args.get('del'):
        task = Task.query.get_or_404(int(request.args.get('del')))
        if task.author_id != current_user.id:
            abort(403)
        task_for_delete = (db.session.query(Task)
                .filter(Task.id == int(request.args.get('del'))).all())
        print()
        db.session.delete(*task_for_delete)
        db.session.commit()
        flash('Задача удалена', 'success')
        return redirect(request.path, code=302)
    else:
        if form.validate_on_submit():
            task_data = Task(title=form.title.data, description=form.description.data, author_id=current_user.id,
                             date=datetime.now())
            db.session.add(task_data)
            db.session.commit()
            flash('Задача добавлена', 'success')
            return redirect(url_for('task'))

    tasks = Task.query.order_by(Task.id)
    return render_template('task.html', title='Simple Manager', form=form, tasks=tasks)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('landing'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваш аккаунт был создан!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('landing'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('landing'))
        else:
            flash('Не получилось войти.', 'danger')
    return render_template('login.html', title='Войти', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('landing'))


@app.errorhandler(403)
@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Страница не найдена')
