from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Length

class RegisterForm(FlaskForm):
    useremail = EmailField('useremail', validators=[DataRequired(), Email()])
    username = StringField('username', validators=[DataRequired('자신의 본명을 입력해주세요.')])
    password = PasswordField('password', validators=[DataRequired('8자 이상, 16자 이하로 작성해주세요.'), Length(min=8, max=16), EqualTo('re_password', '비밀번호가 일치하지 않습니다.')])
    re_password = PasswordField('re_password', validators=[DataRequired()])

class BoardForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수 입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])