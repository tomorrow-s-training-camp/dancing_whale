from flask import Flask, session, render_template, redirect, request, url_for
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# 데이터베이스 값 설정
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '0000'
app.config['MYSQL_DATABASE_DB'] = 'boarddb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.secret_key = "ABCDEFG"
mysql.init_app(app)


@app.route('/', methods=['GET', 'POST'])  # 메인 로그인 화면
def main():
    error = None

    if request.method == 'POST':  # POST 형식으로 요청할 것임
        # 페이지에서 입력한 값을 받아와 변수에 저장
        id = request.form['id']
        pw = request.form['pw']

        conn = mysql.connect()  # DB와 연결
        cursor = conn.cursor()  # connection으로부터 cursor 생성
        sql = "SELECT id FROM users WHERE id = %s AND pw = %s"  # 실행할 SQL문
        value = (id, pw)
        cursor.execute("set names utf8")  # 한글이 정상적으로 출력이 되지 않는 경우를 위해
        cursor.execute(sql, value)  # 메소드로 전달해 명령문을 실행

        data = cursor.fetchall()  # SQL문을 실행한 결과 데이터를 꺼냄
        cursor.close()
        conn.close()

        if data:
            session['login_user'] = id  # 로그인 된 후 페이지로 데이터를 넘기기 위해 session을 사용함
            return redirect(url_for('home'))  # home 페이지로 넘어감 (url_for 메소드를 사용해 home이라는 페이지로 넘어간다)
        else:
            error = 'invalid input data detected !'  # 에러가 발생한 경우

    return render_template('main.html', error=error)


@app.route('/register', methods=['GET', 'POST'])  # 회원가입 화면
def register():
    error = None

    if request.method == 'POST':  # POST 형식으로 요청할 것임
        # 페이지에서 입력한 값을 받아와 변수에 저장
        id = request.form['regi_id']
        pw = request.form['regi_pw']

        conn = mysql.connect()  # DB와 연결
        cursor = conn.cursor()  # connection으로부터 cursor 생성
        sql = "INSERT INTO users VALUES ('%s', '%s')" % (id, pw)  # 실행할 SQL문
        cursor.execute(sql)  # 메소드로 전달해 명령문을 실행
        data = cursor.fetchall()  # 실행한 결과 데이터를 꺼냄

        if not data:
            conn.commit()  # 변경사항 저장
            return redirect(url_for('main'))  # 로그인 화면으로 이동

        else:
            conn.rollback()  # 데이터베이스에 대한 모든 변경사항을 되돌림
            return "Register Failed"

        cursor.close()
        conn.close()

    return render_template('register.html', error=error)  # 용도 확인


@app.route('/home', methods=['GET', 'POST'])  # 로그인 된 후 홈 화면
def home():
    error = None
    id = session['login_user']  # 세션에 저장했던 로그인 유저 아이디를 변수에 저장함

    if request.method == 'POST':  # 게시판에 글 등록하기
        print("POST TEST")
        content = request.form['content']
        conn = mysql.connect()  # DB와 연결
        cursor = conn.cursor()  # connection으로부터 cursor 생성
        sql = "INSERT INTO content (id, content) VALUES ('%s', '%s')" % (id, content)  # 실행할 SQL문
        cursor.execute(sql)  # 메소드로 전달해 명령문을 실행
        new_data = cursor.fetchall()  # 실행한 결과 데이터를 꺼냄

        if not new_data:
            conn.commit()  # 변경사항 저장
            return redirect(url_for("home"))

        else:
            conn.rollback()  # 데이터베이스에 대한 모든 변경사항을 되돌림
            return "Register Failed"

        cursor.close()
        conn.close()

    elif request.method == 'GET':  # 처음 페이지가 로드되는 GET 통신
        conn = mysql.connect()  # DB와 연결
        cursor = conn.cursor()  # connection으로부터 cursor 생성 (데이터베이스의 Fetch 관리)
        sql = "SELECT content, id, times FROM content ORDER BY times desc"  # 실행할 SQL문
        cursor.execute(sql)  # 메소드로 전달해 명령문을 실행
        data = cursor.fetchall()  # 실행한 결과 데이터를 꺼냄

        data_list = []

        for obj in data:  # 튜플 안의 데이터를 하나씩 조회해서
            data_dic = {  # 딕셔너리 형태로
                # 요소들을 하나씩 넣음
                'con': obj[0],
                'writer': obj[1],
                'time': obj[2]
            }
            data_list.append(data_dic)  # 완성된 딕셔너리를 list에 넣음

        cursor.close()
        conn.close()

        return render_template('home.html', error=error, name=id, data_list=data_list)  # html을 렌더하며 DB에서 받아온 값들을 넘김

    return render_template('home.html', error=error, name=id)


if __name__ == '__main__':
    app.run()