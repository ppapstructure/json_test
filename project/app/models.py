from app import db
from sqlalchemy.ext.hybrid import hybrid_property

# 회원정보
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column('username', db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # 로그인을 위한 메서드
    def is_active(self):
        # 조건에 따라 True/False 반환
        return True  

    def get_id(self):
        # 고유 식별자 반환
        return str(self.id)

    @property
    def is_authenticated(self):
        # 사용자 인증 여부
        return True

    @property
    def is_anonymous(self):
        # 익명사용자 유무
        return False
    
    @property
    def username(self):
        return self._username
    # username은 영어로 사용시 전부 소문자
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