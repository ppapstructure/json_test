from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms import StringField,PasswordField,EmailField,TextAreaField

# member_register Form
class CreateUserForm(FlaskForm):
    username = StringField(label ='username', validators=[DataRequired(message='ERR_USERNAEM_REQUIRED'),
                                                           Length(min=3, max=25)])
    password1 = PasswordField(label='password', validators=[
        DataRequired(message='ERR_PASSWORD1_REQUIRED'), EqualTo('password2',
                                                                message= 'ERR_PASSWORD_NOT_CORRECT')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired(message='ERR_PASSWORD2_REQUIRED')])
    email = EmailField('이메일', validators=[DataRequired(message='ERR_EMAIL_REQUIRED'), Email()])

# QuestionForm
class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired(message='ERR_TITLE_REQUIRED')])
    content = TextAreaField('내용', validators=[DataRequired(message='ERR_CONTENT_REQUIRED')])
# AnswerForm
class AnswerForm(FlaskForm):
    content = TextAreaField('답변 내용', validators=[DataRequired(message='ERR_ANSWER_REQUIRED')])

class UserLoginForm(FlaskForm):
    email = EmailField('이메일', validators=[DataRequired(message='ERR_EMAIL_REQUIRED'), Email()])
    password = PasswordField('password', validators=[DataRequired(message='ERR_PASSWORD_REQUIRED')])





