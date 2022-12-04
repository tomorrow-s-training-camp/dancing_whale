# 2022.12.03. 구현 시작일 (코드 작성자 : 이보형) / 버전 2022.12.04. PM 12:00

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import certifi
ca = certifi.where()

from pymongo import MongoClient
client = MongoClient('mongodb+srv://bolee:dancingwhale@cluster0.hezuttp.mongodb.net/?retryWrites=true&w=majority')
db = client.dancingwhale


# 게시글 등록 기능
@app.route("/bolee", methods=["POST"])
def bolee_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    comment_list = list(db.jungmin.find({}, {'_id': False}))
    count = len(comment_list) + 1

    doc = {
        'name':name_receive,
        'comment':comment_receive,
        'num':count,
        'done':0
    }
    db.jungmin.insert_one(doc)

    return jsonify({'msg': '게시글이 등록되었습니다.'})


# 게시글 조회 기능
@app.route("/bolee", methods=["GET"])
def jungmin_get():
    comment_list = list(db.jungmin.find({}, {'_id': False}))
    return jsonify({'jmguestbook': comment_list})


# 게시글 삭제 기능
@app.route("/bolee", methods=["DELETE"])
def delete_jungmin():
    num_receive = request.form['num_give']
    db.jungmin.update_one({'num':int(num_receive)},{'$set':{'done':1}})
    return jsonify({'msg': '게시글이 삭제되었습니다.'})


# 게시글 수정 기능
@app.route("/bolee", methods=["PUT"])
def jungmin_update():
    num_receive = request.form['num_give']
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    db.jungmin.update_one({'num': int(num_receive)}, {'$set': {'name': name_receive}})
    db.jungmin.update_one({'num': int(num_receive)}, {'$set': {'comment': comment_receive}})
    return jsonify({'msg': '게시글이 수정되었습니다!'})