from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db
from sqlalchemy.ext.hybrid import hybrid_property

'''
UserMixin 클래스는 Flask-Login에서 제공하는 클래스로,
User 클래스가 UserMixin 클래스를 상속받으면 Flask-Login에서 제공하는
로그인 관련 메서드를 사용할 수 있게 된다.
is_authenticated, is_active, is_anonymous, get_id 메서드를 자동으로 제공하여
직접 구현할 필요가 없어진다.
'''

# 회원정보
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column('username', db.String(150), unique=True, nullable=False)
    password_hash = db.Column('password',db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    @property
    def password(self):

        # 비밀번호는 읽을 수 없는 속성으로 설정합니다.
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):

        # 비밀번호를 설정할 떄, 해시화하여 저장합니다.
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):

        # 비밀번호가 저장된 해시화된 비밀번호와 일치하는지 확인합니다.
        return check_password_hash(self.password_hash, password)

    @property
    def username(self):
        return self._username
    
    # username은 영어로 사용시 전부 소문자로 저장.
    @username.setter
    def username(self, value):
        self._username = value.lower()

# 질의응답(질문, 답변)
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('questions', lazy=True))
    

    # 질문에 답변이 있는지의 여부를 반환
    @hybrid_property
    def has_answers(self):
        return len(self.answer_set) > 0

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
    question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('answers', lazy=True))