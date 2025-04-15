from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField
from app.models import User, Class
from app.extensions import db


class UserAdmin(ModelView):
    column_list = ['id', 'email', 'role']
    form_columns = ['email', 'password_hash', 'role']
    column_searchable_list = ['email']
    column_filters = ['role']


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
