from flask import Blueprint, request, jsonify
from app.models import User, Class, Enrollment
from app import db
from werkzeug.security import check_password_hash

main = Blueprint('main', __name__)

# Login
@main.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful", "role": user.role, "id": user.id}), 200



# Get Student's Classes
@main.route('/api/student/<int:student_id>/classes')
def get_student_classes(student_id):
    enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    results = []

    for enrollment in enrollments:
        class_ = enrollment.class_
        results.append({
            "id": class_.id,
            "name": class_.name,
            "teacher": class_.teacher.email if class_.teacher else "TBD",
            "time": class_.time if class_.time else "TBD",
            "enrolled": len(class_.enrollments),
            "capacity": class_.capacity,
            "grade": enrollment.grade if enrollment.grade else "N/A"
        })


    return jsonify(results)

# Get All Classes
@main.route('/api/classes')
def get_all_classes():
    classes = Class.query.all()
    results = []
    for class_ in classes:
        results.append({
            "id": class_.id,
            "name": class_.name,
            "teacher": class_.teacher.email if class_.teacher else "TBD",
            "time": class_.time if class_.time else "TBD",
            "enrolled": len(class_.enrollments),
            "capacity": class_.capacity
        })
    return jsonify(results)



# Enrollment
@main.route('/api/student/enroll', methods=['POST'])
def enroll_student():
    data = request.get_json()
    student_id = data.get('student_id')
    class_id = data.get('class_id')

    student = User.query.get(student_id)
    class_ = Class.query.get(class_id)

    if not student or not class_:
        return jsonify({'message': 'Invalid student or class ID'}), 400

    if student.role != 'student':
        return jsonify({'message': 'Only students can enroll'}), 403

    existing = Enrollment.query.filter_by(student_id=student_id, class_id=class_id).first()
    if existing:
        return jsonify({'message': 'Already enrolled'}), 409

    if len(class_.enrollments) >= class_.capacity:
        return jsonify({'message': 'Class is full'}), 400

    enrollment = Enrollment(student_id=student_id, class_id=class_id)
    db.session.add(enrollment)
    db.session.commit()

    return jsonify({'message': 'Enrolled successfully'}), 200


# Unenrollment
@main.route('/api/student/unenroll', methods=['POST'])
def unenroll_student():
    data = request.get_json()
    student_id = data.get('student_id')
    class_id = data.get('class_id')

    enrollment = Enrollment.query.filter_by(student_id=student_id, class_id=class_id).first()
    if not enrollment:
        return jsonify({'message': 'Enrollment not found'}), 404

    db.session.delete(enrollment)
    db.session.commit()
    return jsonify({'message': 'Unenrolled successfully'}), 200


# Classes Taught by Teacher
@main.route('/api/teacher/<int:teacher_id>/classes')
def get_teacher_classes(teacher_id):
    classes = Class.query.filter_by(teacher_id=teacher_id).all()
    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "time": c.time,
            "capacity": c.capacity,
            "enrolled": len(c.enrollments)
        } for c in classes
    ])


# All Student's enrolled in a class
@main.route('/api/class/<int:class_id>/students')
def get_class_students(class_id):
    enrollments = Enrollment.query.filter_by(class_id=class_id).all()
    results = []
    for e in enrollments:
        student = e.student
        results.append({
            "student_id": student.id,
            "email": student.email,
            "grade": e.grade
        })
    return jsonify(results)

# Allow Teacher to update grade
@main.route('/api/class/<int:class_id>/student/<int:student_id>/grade', methods=['POST'])
def update_grade(class_id, student_id):
    data = request.get_json()
    new_grade = data.get('grade')

    enrollment = Enrollment.query.filter_by(class_id=class_id, student_id=student_id).first()
    if not enrollment:
        return jsonify({'message': 'Enrollment not found'}), 404

    enrollment.grade = new_grade
    db.session.commit()
    return jsonify({'message': 'Grade updated'}), 200

@main.route('/logout')
def logout():
    return redirect('/')
