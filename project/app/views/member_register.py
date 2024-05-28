from flask import jsonify, Blueprint
from app.forms import CreateUserForm

from app import db, mail
from app.forms import CreateUserForm
from app.models import User
from flask_mail import Message
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

bp = Blueprint('member_register', __name__)

# GET_ALL
@bp.route('/select_all', methods=['GET'])
def select_all():
    try:
        users = User.query.all()
        if not users:
            return jsonify({'message': 'No users found'}), 404
        return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])
    except SQLAlchemyError as e:
        return jsonify({'message': 'Database error', 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500

# GET_SELECT
@bp.route('/select_one/<int:user_id>', methods=['GET'])
def select_one(user_id):
    if not isinstance(user_id, int):
        return jsonify({'message': 'Invalid user ID format'}), 400
    try:
        user = User.query.filter_by(id=user_id).first()
        if user:
            return jsonify({'id': user.id, 'username': user.username, 'email': user.email})
        else:
            return jsonify({'message': 'User not found'}), 404
    except SQLAlchemyError as e:
        return jsonify({'message': 'Database error', 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500

# POST
@bp.route('/create', methods=['POST'])
def create():
    
    # HTML FORM
    form = CreateUserForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, password=form.password1.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
            
            # 가입 안내 메일 발송
            send_welcome_email(user)  
            return jsonify({'message':'User created successfully'})
        
        except IntegrityError:
            db.session.rollback() 
            return jsonify({'error':'Database error, possibly due to duplicate data.'}), 409
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'message':'Database error', 'error':str(e)}), 500
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'message':'Internal server error', 'error':str(e)}), 500
    else:
        return jsonify({'errors': form.errors}), 400

# 회원가입 직후 가입 안내 메일
def send_welcome_email(user):
    msg = Message('Welcome!', sender='skskfl5786@gmail.com', recipients=[user.email])
    msg.body = f'''Welcome to our service, {user.username}!
We are glad to have you on board.
'''
    mail.send(msg)

# PUT

'''
@bp.route('/update/<int:user_id>',methods=['PUT'])
def update(user_id):
    user = User.query.get(user_id)
    if user:
        form = CreateUserForm()
        if form.validate_on_submit():
            user.username = form.username.data
            user.password = form.password1.data
            user.password = form.password2.data
            user.email = form.email.data
            db.session.commit()
            return jsonify({'message':'User updated successfully'})
        else:
            return jsonify({'error':form.errors}), 400
    else:
        return jsonify({'message':'User not found'}), 404
'''

@bp.route('/update/<int:user_id>', methods=['PUT'])
def update(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        form = CreateUserForm()
        if form.validate_on_submit():
            user.username = form.username.data
            if form.password1.data == form.password2.data:
                user.password = form.password1.data
            else:
                return jsonify({'error': 'Passwords do not match'}), 400
            user.email = form.email.data
            db.session.commit()
            return jsonify({'message': 'User updated successfully'})
        else:
            return jsonify({'errors': form.errors}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), 500


# DELETE
@bp.route('/delete/<int:user_id>',methods=['DELETE'])
def delete(user_id):

    # 특정 ID를 가진 사용자를 데이터베이스에서 조회
    user = User.query.get(user_id) 
    if user:
        db.session.delete(user) 
        db.session.commit()
        return jsonify({'message':'User deleted'})
    else:
        return jsonify({'message':'User not found'}), 404