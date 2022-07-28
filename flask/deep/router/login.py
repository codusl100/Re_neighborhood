from flask import Flask, request, session, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

# 회원가입, 로그인, 로그아웃
app = Flask(__name__)

@app.route('/')
def root():
    return 'root'

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/login_form')
def login_form():
    return render_template('login/login_form.html')

@app.route('/login_proc', methods=['POST'])
def login_proc():
    if request.method == 'POST':
        userId = request.form['id']
        userPwd = request.form['pwd']
        if len(userId) == 0 or len(userPwd) == 0:
            return 'userId, userPwd not found!!'
        else:
            conn = sqlite3.connect('python.db')
            cursor = conn.cursor()
            sql = 'select idx, userId, userPwd, userEmail from member where userId = ?'
            cursor.execute(sql, (userId, ))
            rows = cursor.fetchall()
            for rs in rows:
                if userId == rs[1] and userPwd == rs[2]:
                    session['logFlag'] = True
                    session['idx'] = rs[0]
                    session['userId'] = userId
                    return redirect(url_for('main'))
                else:
                    return redirect(url_for('login_form')) #메소드를 호출
    else:
        return '잘못된 접근입니다.'

@app.route('/user_info_edit/<int:edit_idx>', methods=['GET'])
def getUser(edit_idx):
    if session.get('logFlag') != True:
        return redirect('login_form')
    conn = sqlite3.connect('python.db')
    cursor = conn.cursor()
    sql = 'select userEmail from member where idx = ?'
    cursor.execute(sql, (edit_idx,))
    row = cursor.fetchone()
    edit_email = row[0]
    cursor.close()
    conn.close()
    return render_template('users/user_info.html', edit_idx=edit_idx, edit_email=edit_email)

@app.route('/user_info_edit_proc', methods=['POST'])
def user_info_edit_proc():
    idx = request.form['idx']
    userPwd = request.form['userPwd']
    userEmail = request.form['userEmail']
    if len('idx') == 0:
        return 'Edit Data Not Found'
    else:
        conn = sqlite3.connect('python.db')
        cursor = conn.cursor()
        sql = 'update member set userPwd = ?, userEmail = ? where idx = ?'
        cursor.execute(sql, (userPwd, userEmail, idx))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('main'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.secret_key = '20220727'
    app.debug = True
    app.run()
