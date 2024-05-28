from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from app.models import User
from app.forms import UserLoginForm

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    form = UserLoginForm(request.form)
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            return jsonify(success=True, message='login success')
        else:
            return jsonify(success=False, message='Login failed. Please check your email or password.')
    else:
        return jsonify(success=False, message='Input value is invalid.')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(success=True, message='logout success')