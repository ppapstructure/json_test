from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
import config

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()

def create_app():

    app = Flask(__name__)
    app.config.from_object(config)
    
    # ORM, Email
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    
    # Blueprint
    from app.views import member_register
    from app.views import auth_views
    from app.views import question_views
    from app.views import answer_views
    
    app.register_blueprint(member_register.bp, url_prefix='/member')
    app.register_blueprint(auth_views.bp, url_prefix='/auth')
    app.register_blueprint(question_views.bp, url_prefix='/question')
    app.register_blueprint(answer_views.bp, url_prefix='/answer')

    # User loader settings
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify(message='You must be logged in to access this resource'), 401

    return app