import os  # 절대경로를 지정하기 위한 Os모듈 임포트
from flask import Flask
from flask import request  # 회원정보 제출했을때 받아오기 위한 request, post요청을 활성화시키기 위함
from flask import redirect  # 페이지 이동시키는 함수
from flask import render_template
from models import db
from models import Fcuser  # 모델의 클래스 가져오기.

from flask_wtf.csrf import CSRFProtect
from form import RegisterForm

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():  # POST검사의 유효성검사

        user = Fcuser()
        user.useremail = form.data.get('useremail')
        user.username = form.data.get('username')
        user.password = form.data.get('password')

        db.session.add(user)  # 회원정보 DB에 저장
        db.session.commit()
        return "가입 완료"

    return render_template('register.html', form=form)


if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__)) # db파일 절대경로
    dbfile = os.path.join(basedir, 'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'qwejhqoifuas'

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)
    db.app = app
    db.create_all()  # db 생성

    app.run(host='127.0.0.1', port=5000, debug=True)