# Database models: User, Course, Enrollment, etc.
from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student', 'teacher', 'admin'
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def __str__(self):
        return self.email


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    enrollments = db.relationship('Enrollment', backref='class_', lazy=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    teacher = db.relationship('User', backref='classes', foreign_keys=[teacher_id])
    time = db.Column(db.String(100))  

    def __repr__(self):
        return f'<Class {self.name}>'

    def __str__(self):
        return self.name


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    grade = db.Column(db.String(5))

    def __repr__(self):
        return f'<Enrollment {self.student.email} in {self.class_.name}>'
