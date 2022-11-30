from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import db, app
from .models import Student, Course, User
from .forms import StudentForm, CourseForm, UserForm


def students_list():
    students = db.session.query(Student, Course).join(Course).all()
    return render_template('students_list.html', students=students)

def courses_list():
    courses = Course.query.all()
    return render_template('courses_list.html', courses=courses)

@login_required
def student_create():
    form = StudentForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            student = Student()
            form.populate_obj(student)
            db.session.add(student)
            db.session.commit()
            flash('Student succesfully saved!', 'success')
            return redirect(url_for('students_list'))
    return render_template('student_form.html', form=form)

@login_required
def course_create():
    form = CourseForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            course = Course()
            form.populate_obj(course)
            db.session.add(course)
            db.session.commit()
            return redirect(url_for('courses_list'))
    return render_template('course_form.html', form=form)

def student_detail(id):
    student = Student.query.get(id)
    return render_template('student_detail.html', student=student)

def course_detail(id):
    course = Course.query.get(id)
    return render_template('course_detail.html', course=course)

@login_required
def student_update(id):
    student = Student.query.get(id)
    form = StudentForm(request.form, obj=student)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(student)
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('students_list'))
    return render_template('student_form.html', form=form)

@login_required
def course_update(id):
    course = Course.query.get(id)
    form = CourseForm(request.form, obj=course)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(course)
            db.session.add(course)
            db.session.commit()
            return redirect(url_for('courses_list'))
    return render_template('course_form.html', form=form)

@login_required
def student_delete(id):
    student = Student.query.get(id)
    if request.method == 'POST':
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('students_list'))
    return render_template('student_delete.html', student=student)

@login_required
def course_delete(id):
    course = Course.query.get(id) ###object kotor obnovl
    if request.method == 'POST':
        db.session.delete(course)
        db.session.commit()
        return redirect(url_for('courses_list'))
    return render_template('course_delete.html', course=course)

def register_view():
    form = UserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User()
            form.populate_obj(user)
            # user = User(username=request.form.get('username'))
            # user.set_password(request.form.get('password'))
            db.session.add(user)
            db.session.commit()
            flash(f'User {user.username} successfully registered!', 'success')
            return redirect(url_for('login'))
    return render_template('user_form.html', form=form)

def login_view():
    logout_user()
    form = UserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=request.form.get('username')).first()
            if user and user.check_password(request.form.get('password')):
                login_user(user)
                flash('Successfully authorized!', 'primary')
                return redirect(url_for('students_list'))
            else:
                flash('Incorrect login or password', 'danger')
    return render_template('login_form.html', form=form)


def logout_view():
    form = UserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=request.form.get('username')).first()
            if user and user.check_password(request.form.get('password')):
                logout_user()
                flash('Successfully logout!', 'primary')
                return redirect(url_for('login'))
            else:
                flash('Incorrect login or password', 'danger')
    return render_template('logout_form.html', form=form)
# def logout_view():
#     logout_user()
#     return redirect(url_for('login'))
