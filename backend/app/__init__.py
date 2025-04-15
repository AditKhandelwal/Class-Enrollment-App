from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import User, Class, Enrollment
from app.extensions import db
from app.admin_views import UserAdmin, ClassAdmin, EnrollmentAdmin

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enrollment.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret-key'

    db.init_app(app)
    CORS(app)

    from .routes import main
    app.register_blueprint(main)

    # Set up Flask-Admin
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(ClassAdmin(Class, db.session))
    admin.add_view(EnrollmentAdmin(Enrollment, db.session))
    
    return app