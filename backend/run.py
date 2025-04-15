from app import create_app, db
from app.models import User, Class

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates tables if they don't exist

        if not User.query.first():
            from werkzeug.security import generate_password_hash

            users = [
                User(email="student@example.com", password_hash=generate_password_hash("student123"), role="student"),
                User(email="teacher@example.com", password_hash=generate_password_hash("teacher123"), role="teacher"),
                User(email="admin@example.com", password_hash=generate_password_hash("admin123"), role="admin"),
            ]
            db.session.bulk_save_objects(users)
            db.session.commit()
            print("Sample users added")

        if not Class.query.first():
            classes = [
                Class(name="Intro to Python", capacity=3),
                Class(name="Data Structures", capacity=2),
                Class(name="Web Development", capacity=4)
            ]
            db.session.bulk_save_objects(classes)
            db.session.commit()
            print("Sample classes added")

    app.run(debug=True)
