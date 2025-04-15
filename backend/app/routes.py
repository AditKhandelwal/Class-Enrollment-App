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

    return jsonify({"message": "Login successful", "role": user.role}), 200


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
            "teacher": "TBD",  # Add teacher association later
            "time": "TBD",     # Add schedule later
            "enrolled": len(class_.enrollments),
            "capacity": class_.capacity
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
            "teacher": "TBD",  # To be updated later
            "time": "TBD",     # To be updated later
            "enrolled": len(class_.enrollments),  # ✅ This is the key line
            "capacity": class_.capacity
        })
    return jsonify(results)


# Enrollment
@main.route('/api/student/enroll', methods=['POST'])
def enroll_student():
    data = request.get_json()
    student_id = data.get('student_id')
    class_id = data.get('class_id')

    # Validate
    student = User.query.get(student_id)
    class_ = Class.query.get(class_id)

    if not student or not class_:
        return jsonify({'message': 'Invalid student or class ID'}), 400

    if student.role != 'student':
        return jsonify({'message': 'Only students can enroll'}), 403

    # Check if already enrolled
    existing = Enrollment.query.filter_by(student_id=student_id, class_id=class_id).first()
    if existing:
        return jsonify({'message': 'Already enrolled'}), 409

    # Check capacity
    if len(class_.enrollments) >= class_.capacity:
        return jsonify({'message': 'Class is full'}), 400

    # Enroll
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
