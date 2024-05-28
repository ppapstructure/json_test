from datetime import datetime

from flask import jsonify, Blueprint
from flask_login import login_required, current_user
from app.forms import QuestionForm

from app import db
from app.models import Question

from sqlalchemy.exc import IntegrityError,SQLAlchemyError

bp = Blueprint('question', __name__)

# GET ALL -> 전체 질문 리스트 조회
@bp.route('/list/', methods=['GET'])
def _list():
    try:
        question_lists = Question.query.order_by(Question.create_date.desc()).all()
        if not question_lists:
            return jsonify({'message': 'No questions found'}), 404
        result = []
        for question in question_lists:
            question_data = {
                'id': question.id,
                'subject': question.subject,
                'content': question.content,
                'create_date': question.create_date,
                'writer': question.user.email 
            }
            result.append(question_data)
        return jsonify(result)
    except SQLAlchemyError as e:
        return jsonify({'message': 'Database error', 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500

# GET ONE -> 특정 질문 조회
@bp.route('/detail/<int:question_id>/', methods=['GET'])
def detail(question_id):
    try:
        question = Question.query.get(question_id)
        if not question:
            return jsonify({'message': 'Question not found'}), 404
        
        question_data = {
            'id': question.id,
            'subject': question.subject,
            'content': question.content,
            'answers': [{'id': answer.id, 'content': answer.content, 'create_date': answer.create_date, 
                         'writer': answer.user.email} for answer in question.answer_set],
            'create_date': question.create_date,
            'writer': question.user.email,
            'has_answers': question.has_answers
        }
        return jsonify(question_data)
    except SQLAlchemyError as e:
        return jsonify({'message': 'Database error', 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500
    
# POST
@bp.route('/create/', methods=['POST'])
@login_required
def create():
    form = QuestionForm()
    if form.validate_on_submit():
        try:
            question = Question(subject=form.subject.data, content=form.content.data,
                                create_date=datetime.now(), user_id=current_user.id)
            db.session.add(question)
            db.session.commit()
            return jsonify({'message':'Question created successfully'})
        
         # 데이터베이스 제약 조건 위배 시 처리
        except IntegrityError: 
            db.session.rollback()
            return jsonify({'error':'Database error, possibly due to duplicate data.'}), 409
        
        # 데이터베이스 에러
        except SQLAlchemyError as e: 
            db.session.rollback()
            return jsonify({'message':'Database error', 'error':str(e)}), 500
        
        # 그 외 에러
        except Exception as e: 
            db.session.rollback()
            return jsonify({'message':'Internal server error', 'error':str(e)}), 500
    else:
        return jsonify({'errors': form.errors}), 400

# 내 계정이 아닐경우, 우선은 수정/삭제 불가능함
# 그러나 내 계정이 아닐경우 수정, 삭제 안보이게 할수 있으면 더 좋을 것 같음
# PUT
@bp.route('/update/<int:question_id>', methods=['PUT'])
@login_required
def update(question_id):
    try:
        question = Question.query.get(question_id)
        if not question:
            return jsonify({"message": "Question not found"}), 404
        if question.user_id != current_user.id:
            return jsonify({"message": "This is not your post"}), 403
        
        form = QuestionForm()
        if form.validate_on_submit():
            question.subject = form.subject.data
            question.content = form.content.data
            db.session.commit()
            return jsonify({"message": "Question updated successfully"})
        else:
            return jsonify({"errors": form.errors}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), 500


# DELETE
@bp.route('/delete/<int:question_id>', methods=['DELETE'])
@login_required
def delete(question_id):
    try:
        question = Question.query.get(question_id)
        if not question:
            return jsonify({'message':'Question not found'}), 404
        if question.user_id != current_user.id:
            return jsonify({'message':'This is not your post'}), 403
        
        db.session.delete(question)
        db.session.commit()
        return jsonify({'message':'Question deleted'})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message':'Database error', 'error':str(e)}), 500
    except Exception as e:
        return jsonify({'message':'Internal server error', 'error':str(e)}), 500
        