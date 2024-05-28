from datetime import datetime

from flask import jsonify, Blueprint
from flask_login import login_required, current_user
from app.forms import QuestionForm, AnswerForm

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
        question = Question.query.get_or_404(question_id)
        question_data = {
            'id': question.id,
            'subject': question.subject,
            'content': question.content,
            'answers': [{'id': answer.id, 'content': answer.content, 'create_date': answer.create_date, 'writer': answer.user.email}
                        for answer in question.answer_set],
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
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error':'Database error, possibly due to duplicate data.'}), 409
    else:
        return jsonify({'errors': form.errors}), 400

# PUT
@bp.route('/update/<int:question_id>',methods=['PUT'])
@login_required
def update(question_id):
    question = Question.query.get(question_id)
    if question and question.user_id == current_user.id:
        form = QuestionForm()
        if form.validate_on_submit():
            question.subject = form.subject.data
            question.content = form.content.data
            db.session.commit()
            return jsonify({'message':'Question updated successfully'})
        else:
            return jsonify({'error':form.errors}), 400
    elif question.user_id != current_user.id:
        return jsonify({'message':'This is not your post'}), 404
    else:
        return jsonify({'message':'Question not found'}), 404

# DELETE
# 질문 삭제시 질문에 연결된 답변도 같이 삭제되어야 함
@bp.route('/delete/<int:question_id>', methods=['DELETE'])
@login_required
def delete(question_id):
    question = Question.query.get(question_id)
    if question and question.user_id == current_user.id:
        db.session.delete(question) 
        db.session.commit()  
        return jsonify({'message':'Question deleted'})
    elif question.user_id != current_user.id:
        return jsonify({'message':'This is not your post'}), 404    
    else:
        return jsonify({'message':'Question not found'}), 404