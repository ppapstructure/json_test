import traceback
from datetime import datetime

from flask import jsonify, Blueprint
from flask_login import login_required, current_user
from app.forms import QuestionForm, AnswerForm

from app import db
from app.models import Answer,Question

from sqlalchemy.exc import IntegrityError

bp = Blueprint('answer', __name__)

# GET ALL
@bp.route('/list/', methods=['GET'])
def _list():
    answer_lists = Answer.query.order_by(Answer.create_date.desc())
    return jsonify([{'id': answer_list.id,'question_id': answer_list.question_id,'content': answer_list.content,
                    'create_date':answer_list.create_date} for answer_list in answer_lists])    

# GET ONE -> 특정 답변 조회
@bp.route('/detail/<int:answer_id>/', methods=['GET'])
def detail(answer_id):
    answer = Answer.query.get_or_404(answer_id)

    return jsonify({
        'id': answer.id,
        'question_id': answer.question_id,
        'content': answer.content,
        'create_date': answer.create_date,
        'question' : {
            'id': answer.question.id,
            'subject': answer.question.subject,
            'content': answer.question.content,
            'create_date': answer.question.create_date
        }
    })

# POST
@bp.route('/create/<int:question_id>', methods=['POST'])
@login_required
def create(question_id):
    form = AnswerForm()
    if form.validate_on_submit():
        try:
            question = Question.query.get_or_404(question_id)
            answer = Answer(content=form.content.data, create_date=datetime.now(), question_id=question.id, user_id=current_user.id)
            db.session.add(answer)
            db.session.commit()
            return jsonify({'message': 'Answer created successfully'})
        
        except IntegrityError as e:
            db.session.rollback()
            error_message = traceback.format_exc()  # 디버그 정보를 출력합니다.
            print(error_message)
            return jsonify({'error': 'Database error, possibly due to duplicate data.','details':error_message}), 409
    else:
        return jsonify({'errors': form.errors}), 400
    
# PUT
@bp.route('/update/<int:answer_id>', methods=['PUT'])
@login_required
def update(answer_id):
    answer = Answer.query.get(answer_id)
    if answer and answer.user_id == current_user.id:
        form = AnswerForm()
        if form.validate_on_submit():
            answer.content = form.content.data
            db.session.commit()
            return jsonify({'message':'Answer updated successfully'})
        else:
            return jsonify({'error':form.errors}), 400
    else:
        return jsonify({'message':'Answer not found'}), 404

# DELETE
@bp.route('/delete/<int:answer_id>', methods=['DELETE'])
@login_required
def delete(answer_id):
    answer = Answer.query.get(answer_id) # 특정 ID를 가진 사용자를 데이터베이스에서 조회
    if answer and answer.user_id == current_user.id:
        db.session.delete(answer)
        db.session.commit()
        return jsonify({'message': 'Answer deleted successfully'})
    else:
        db.session.rollback()
        return jsonify({'message':'Answer not found'}), 404