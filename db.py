import sqlite3
path_db = r'mysite/db/main.db'

# mp3ファイルの情報をdatabaseに登録する
def put_mp3info(user, filename, hashtext, size):

    con = sqlite3.connect(path_db)
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO file VALUES (?, ?, ?, ?)",(user, filename, hashtext, size))
    except sqlite3.Error as e:
    	print(e)
    con.commit()
    con.close()

# mp3ファイルの情報をdatabaseにから削除する
def del_mp3info(filename):

    con = sqlite3.connect(path_db)
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM file WHERE filename = ?", (filename,))
    except sqlite3.Error as e:
    	print(e)
    con.commit()
    con.close()

# mp3ファイルの情報をdatabaseから取得する
def get_mp3info_list():
    con = sqlite3.connect(path_db)
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM file")
    except sqlite3.Error as e:
        print(e)
    list = cur.fetchall()
    con.commit()
    con.close()
    return list
