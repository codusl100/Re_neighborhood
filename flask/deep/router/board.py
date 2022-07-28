from flask import Flask, request, session, render_template, redirect, url_for
import sqlite3

# 게시물 업로드
@app.route('/post/upload', methods=['POST'])
def upload_post():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    doc = {
        'title': title_receive,
        'content': content_receive,
        'like': 0
    }

    db.posts.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '업로드 완료!'})

# 게시물 보여주기

@app.route('/post/list', methods=['GET'])
def view_post():
    posts = list(db.posts.find({}, {'_id': False}))

    return jsonify({'result': 'success', 'all_posts': posts})

# 게시물 삭제

@app.route('/post/delete', methods=['POST'])
def delete_post():
    title_receive = request.form['title_give']
    db.posts.delete_one({'title': title_receive})

    return jsonify({'result': 'success', 'msg': '삭제 완료!'})