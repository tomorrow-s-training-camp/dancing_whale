# GET -> 유지되고있는 username 세션과 현재 접속되어진 id와 일치시 edit페이지 연결
# POST -> 접속되어진 id와 일치하는 title, content를 찾아 UPDATE

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
    return render_template('Error.html')
