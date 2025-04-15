from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField, SelectField
from app.models import User, Class
from app.extensions import db
from flask_admin import BaseView, expose
from flask import redirect
from werkzeug.security import generate_password_hash

class LogoutAdminView(BaseView):
    @expose('/')
    def index(self):
        return redirect('http://localhost:5173/login')

class UserAdmin(ModelView):
    column_list = ['id', 'email', 'role']
    form_columns = ['email', 'password', 'role']
    column_searchable_list = ['email']
    column_filters = ['role']
    
    form_extra_fields = {
        'password': PasswordField('Password')
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password_hash = generate_password_hash(form.password.data)
        return super().on_model_change(form, model, is_created)

class ClassAdmin(ModelView):
    column_list = ['id', 'name', 'teacher', 'capacity', 'time']
    form_columns = ['name', 'teacher_id', 'capacity', 'time']
    form_overrides = {'teacher_id': SelectField}

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.teacher_id.choices = [(t.id, t.email) for t in User.query.filter_by(role='teacher').all()]
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.teacher_id.choices = [(t.id, t.email) for t in User.query.filter_by(role='teacher').all()]
        return form

class EnrollmentAdmin(ModelView):
    column_list = ['id', 'student', 'class_', 'grade']
    form_columns = ['student_id', 'class_id', 'grade']
    form_overrides = {
        'student_id': SelectField,
        'class_id': SelectField
    }

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.student_id.choices = [(s.id, s.email) for s in User.query.filter_by(role='student').all()]
        form.class_id.choices = [(c.id, c.name) for c in Class.query.all()]
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.student_id.choices = [(s.id, s.email) for s in User.query.filter_by(role='student').all()]
        form.class_id.choices = [(c.id, c.name) for c in Class.query.all()]
        return form