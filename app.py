from flask import Flask, render_template, session, url_for, request, redirect
import pymysql
import hashlib

'''
# 로깅시스템 - 시작
import logging
import datetime
from pytz import timezone
# 로깅시스템 - 끝 (인터프리터 pytz)
'''
app = Flask(__name__)
app.secret_key = '1234'

'''
# 로깅시스템 - 시작
logging.basicConfig(filename = "logs/test.log", level = logging.DEBUG)

def log(request, message):
    log_date = get_log_date()
    log_message = "{0}/{1}/{2}".format(log_date, str(request), message)
    logging.error(log_message)
def error_log(request, error_code, error_message):
    log_date = get_log_date()
    log_message = "{0}/{1}/{2}/{3}".format(log_date, str(request), error_code, error_message)
    logging.error(log_message)

def get_log_date():
    dt = datetime.datetime.now(timezone("Asia/Seoul"))
    log_date = dt.strftime("%Y%m%d_%H:%M:%S")
    return log_date
# 로깅시스템 - 끝
'''

def connectsql():
    conn = pymysql.connect(host='localhost', user = 'root', passwd = '0000', db = 'userlist', charset='utf8')
    return conn

@app.route('/')
# 세션유지를 통한 로그인 유무 확인
def index():
    if 'username' in session:
        username = session['username']

        return render_template('index.html', logininfo = username)
    else:
        username = None
        return render_template('index.html', logininfo = username )

@app.route('/post')
# board테이블의 게시판 제목리스트 역순으로 출력
def post():
    if 'username' in session:
        username = session['username']
    else:
        username = None
    conn = connectsql()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT id, name, title, content, wdate, view FROM board ORDER BY id DESC" # ORDER BY 컬럼명 DESC : 역순출력, ASC : 순차출력
    cursor.execute(query)
    post_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('post.html', postlist = post_list, logininfo=username)

# mydata


@app.route('/post/content/<id>')
# 조회수 증가, post페이지의 게시글 클릭시 id와 content 비교 후 게시글 내용 출력
def content(id):
    if 'username' in session:
        username = session['username']
        conn = connectsql()
        cursor = conn.cursor()
        query = "UPDATE board SET view = view + 1 WHERE id = %s"
        value = id
        cursor.execute(query, value)
        conn.commit()
        cursor.close()
        conn.close()

        conn = connectsql()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT id, name, title, content, view FROM board WHERE id = %s"
        value = id
        cursor.execute(query, value)
        content = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('content.html', data = content, username = username)
    else:
        return render_template ('Error.html')

@app.route('/post/edit/<id>', methods=['GET', 'POST'])
# GET -> 유지되고있는 username 세션과 현재 접속되어진 id와 일치시 edit페이지 연결
# POST -> 접속되어진 id와 일치하는 title, content를 찾아 UPDATE
def edit(id):
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']

            edittitle = request.form['title']
            editcontent = request.form['content']

            conn = connectsql()
            cursor = conn.cursor()
            query = "UPDATE board SET title = %s, content = %s WHERE id = %s"
            value = (edittitle, editcontent, id)
            cursor.execute(query, value)
            conn.commit()
            cursor.close()
            conn.close()

            return render_template('editSuccess.html')
    else:
        if 'username' in session:
            username = session['username']
            conn = connectsql()
            cursor = conn.cursor()
            query = "SELECT name FROM board WHERE id = %s"
            value = id
            cursor.execute(query, value)
            data = [post[0] for post in cursor.fetchall()]
            cursor.close()
            conn.close()

            if username in data:
                conn = connectsql()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                query = "SELECT id, title, content FROM board WHERE id = %s"
                value = id
                cursor.execute(query, value)
                postdata = cursor.fetchall()
                cursor.close()
                conn.close()
                return render_template('edit.html', data=postdata, logininfo=username)
            else:
                return render_template('editError.html')
        else:
            return render_template ('Error.html')

@app.route('/post/delete/<id>')
# 유지되고 있는 username 세션과 id 일치시 삭제확인 팝업 연결
def delete(id):
    if 'username' in session:
        username = session['username']
        conn = connectsql()
        cursor = conn.cursor()
        query = "SELECT name FROM board WHERE id = %s"
        value = id
        cursor.execute(query, value)
        data = [post[0] for post in cursor.fetchall()]
        cursor.close()
        conn.close()

        if username in data:
            return render_template('delete.html', id = id)
        else:
            return render_template('editError.html')
    else:
        return render_template ('Error.html')

@app.route('/post/delete/success/<id>')
# 삭제 확인시 id와 일치하는 컬럼 삭제, 취소시 /post 페이지 연결
def deletesuccess(id):
    conn = connectsql()
    cursor = conn.cursor()
    query = "DELETE FROM board WHERE id = %s"
    value = id
    cursor.execute(query, value)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('post'))

@app.route('/write', methods=['GET', 'POST'])
# GET -> write 페이지 연결
# POST -> username, password를 세션으로 불러온 후, form에 작성되어진 title, content를 테이블에 입력
def write():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            password = session['password']

            usertitle = request.form['title']
            usercontent = request.form['content']

            conn = connectsql()
            cursor = conn.cursor()
            query = "INSERT INTO board (name, pass, title, content) values (%s, %s, %s, %s)"
            value = (username, password, usertitle, usercontent)
            cursor.execute(query, value)
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('post'))
        else:
            return render_template('errorpage.html')
    else:
        if 'username' in session:
            username = session['username']
            return render_template ('write.html', logininfo = username)
        else:
            return render_template ('Error.html')

@app.route('/logout')
# username 세션 해제
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET','POST'])
# GET -> 로그인 페이지 연결
# POST -> 로그인 시 form에 입력된 id, pw를 table에 저장된 id, pw에 비교후 일치하면 로그인, id,pw 세션유지
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #username = request.form['user_name']
        #userpwd = request.form['pwd']

        logininfo = request.form['username']
        conn = connectsql()
        cursor = conn.cursor()
        query = "SELECT * FROM user WHERE user_name = %s AND user_pwd = %s"
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        value = (username, password)
        cursor.execute(query, value)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        for row in data:
            data = row[0]

        if data:
            session['username'] = request.form['username']
            session['password'] = request.form['password']

            #session['username'] = request.form['name']
            #session['userpwd'] = request.form['pwd']

            return render_template('index.html', logininfo = logininfo)
        else:
            return render_template('loginError.html')
    else:
        return render_template ('login.html')

@app.route('/regist', methods=['GET', 'POST'])
# GET -> 회원가입 페이지 연결
# 회원가입 버튼 클릭 시, 입력된 id가 tbl_user의 컬럼에 있을 시 에러팝업, 없을 시 회원가입 성공
def regist():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        userintro = request.form['intro']
        #userid = request.form['id']
        #userpw = request.form['pw']

        conn = connectsql()
        cursor = conn.cursor()
        query = "SELECT * FROM user WHERE user_name = %s" # 아이디(username) 중복 검사 부분
        value = username
        cursor.execute(query, value)
        data = (cursor.fetchall())
        #import pdb; pdb.set_trace()
        if data:
            conn.rollback() # 이건 안 써도 될 듯
            return render_template('registError.html')
        else:
            query = "INSERT INTO user (user_name, user_pwd, user_intro) values (%s, %s, %s)"
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            value = (username, password, userintro)
            cursor.execute(query, value)
            data = cursor.fetchall()
            conn.commit()
            return render_template('registSuccess.html')
        cursor.close()
        conn.close()
    else:
        return render_template('regist.html')

# # 마이페이지로 가는 버튼 부분 테스트 - 시작
# @app.route('/mypage/<myid>')
# # GET -> 유지되고있는 username 세션과 현재 접속되어진 id와 일치시 edit페이지 연결
# # POST -> 접속되어진 id와 일치하는 title, content를 찾아 UPDATE
# def mydata(myid):
#     if 'username' in session:
#         username = session['username']
#
#         conn = connectsql()
#         cursor = conn.cursor()
#         query = f"SELECT user_name, user_intro FROM user WHERE user_name = '{myid}'" # where user_id로 잘못써서 mysql에서 데이터 안나옴
#         print(query)
#         cursor.execute(query)
#         data = [myinfo[0] for myinfo in cursor.fetchall()]
#         print(data)
#         cursor.close()
#         conn.close()
#         return render_template('mypage.html', mydatalist=mydata, logininfo=username)
#
#         # if username in data:
#         #     conn = connectsql()
#         #     cursor = conn.cursor(pymysql.cursors.DictCursor)
#         #     query = f"SELECT user_name, user_intro FROM user WHERE user_name = '{myid}'" # where user_id로 잘못써서 mysql에서 데이터 안나옴
#         #     print(query)
#         #     cursor.execute(query)
#         #     mydata = cursor.fetchall()
#         #     print(mydata)
#         #     cursor.close()
#         #     conn.close()
#         #     return render_template('mypage.html', mydatalist=mydata, logininfo=username)
#        # else:
#         #    return render_template('editError.html') # 본인게시글이 아닙니다!
#     else:
#         return render_template ('Error.html') # 로그인하세요!
# # 마이페이지로 가는 버튼 부분 테스트 - 끝


마이페이지 - 테스트

    array = cursor.fetchall()
        for i in range(len(array)):
            print(array[i])
            print(len(array))

           print(array[i]['user_name'])
           print(array[i]['user_intro'])

        user_name, user_intro = cursor.fetchone()
        print(user_name)
        print(user_intro)
        mycontent = [myinfo[0] for myinfo in cursor.fetchall()] fetchall 왜쓰냐.. 유저들, 전체검색할때임 한명일땐 fetchone
        print(mycontent)

@app.route('/mypage/<myid>')
def mycontent(myid):
    if 'username' in session:
        username = session['username']
        conn = connectsql()
        # cursor = conn.cursor()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = f"SELECT user_name, user_intro FROM user WHERE user_name = '{myid}'"  # where user_id로 잘못써서 mysql에서 데이터 안나옴
        print(query)

        cursor.execute(query)
        result = cursor.fetchone()
        # print(result)
        print(result['user_name'])
        print(result['user_intro'])

        cursor.close()
        conn.close()

        return render_template('mypage.html', mydata = 'result', username = username)


# # 마이페이지 - 잘 작동하는 코드 (post.html에서 링크 눌렀을 때 mypage.html과 연결안됨)
# @app.route('/mypage/<myid>')
# # 페이지의 게시글 클릭시 id와 content 비교 후 게시글 내용 출력
# def mycontent(myid):
#     if 'username' in session:
#         username = session['username']
#
#         conn = connectsql()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         # query = "SELECT user_name, user_intro FROM user WHERE user_id"
#         query = f"SELECT user_name, user_intro FROM user WHERE user_name = '{myid}'"
#         cursor.execute(query)
#         mycontent = cursor.fetchall()
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return render_template('mypage.html', mydata = mycontent, username = username)
#     else:
#         return render_template ('Error.html')


@app.route('/mypage/edit/<myid>', methods=['GET', 'POST'])
# GET -> 유지되고있는 username 세션과 현재 접속되어진 id와 일치시 edit페이지 연결
# POST -> 접속되어진 id와 일치하는 title, content를 찾아 UPDATE
def mycontentedit(myid):
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']

            myusername = request.form['user_name']
            myuserintro = request.form['user_intro']

            conn = connectsql()
            cursor = conn.cursor()
            query = f"UPDATE user SET user_name = %s, user_intro = %s WHERE user_name = '{myid}'"
            #value = (myusername, myuserintro)
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()

            return render_template('editSuccess.html')
    else:
        if 'username' in session:
            username = session['username']
            conn = connectsql()
            cursor = conn.cursor()
            query = f"SELECT user_name, user_intro FROM user WHERE user_name = '{myid}'" # where user_id로 잘못써서 mysql에서 데이터 안나옴
            cursor.execute(query)
            data = [myinfo[0] for myinfo in cursor.fetchall()]
            cursor.close()
            conn.close()

            if username in data:
                conn = connectsql()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                query = f"SELECT user_name, user_intro FROM user WHERE user_name = '{myid}'" # where user_id로 잘못써서 mysql에서 데이터 안나옴
                cursor.execute(query)
                mycontentedit = cursor.fetchall()
                cursor.close()
                conn.close()
                return render_template('mypageEdit.html', mydataedit=mycontentedit, logininfo=username)
            else:
                return render_template('editError.html') # 본인게시글이 아닙니다!
        else:
            return render_template ('Error.html') # 로그인하세요!

if __name__ == '__main__':
    app.run(debug=True)