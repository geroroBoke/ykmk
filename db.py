import sqlite3
from mp3 import dir_mp3
import os

path_db = r'mysite/db/main.db'
# CREATE TABLE file (user text, filename text, hash text, size integer);
# CREATE TABLE queue (user text, filename text, text text, flag text);

# mp3ファイルの情報をdatabaseに登録する
def put_mp3info(user, filename, hash, size):

    con = sqlite3.connect(path_db)
    cur = con.cursor()

    # 同一ファイルがあるか確認する
    flagAlready = False;
    cur.execute("SELECT * from file where filename = ?", (filename,))
    if len(cur.fetchall()):
        flagAlready = True;

    # 同一ファイル名があればアップデートする
    if flagAlready:
        cur.execute("UPDATE file SET user = ?, hash = ?, size = ? where filename = ?",(user, hash, size, filename))

    # 無ければインサートする
    else:
        cur.execute("INSERT INTO file (user, filename, hash, size) VALUES (?, ?, ?, ?)",(user, filename, hash, size))

    con.commit()
    con.close()

# 同一ハッシュのmp3があるか確認する
def check_mp3info_exist(hash):

    con = sqlite3.connect(path_db)
    cur = con.cursor()

    # 同一hashがあるか確認する
    flagAlready = False;
    cur.execute("SELECT * from file where hash = ?", (hash,))
    if len(cur.fetchall()):
        flagAlready = True;
    con.close()
    return flagAlready

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
def get_mp3info_lists():

    # # ファイルの存在とDBの整合性を保つ
    keep_mp3info_consistency()

    con = sqlite3.connect(path_db)
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM file")
    except sqlite3.Error as e:
        print(e)
        return
    lists = cur.fetchall()
    con.close()
    return lists

# ファイルの存在とDBの整合性を保つ
def keep_mp3info_consistency():

    # filenameのリストを取得する
    con = sqlite3.connect(path_db)
    cur = con.cursor()
    try:
        cur.execute("SELECT filename FROM file")
    except sqlite3.Error as e:
        print(e)
        return
    lists = cur.fetchall()
    con.close()

    # filenameのファイルが存在しなければ、レコードを消す
    for l in lists:
        filename = l[0]
        if not os.path.exists(dir_mp3 + filename):
            del_mp3info(filename)
            print("keep_mp3info_consistency: drop records of " + filename)


# 変換待ちのテキストキューに追加する
def put_textqueue(user, filename, text):

    # execute sql
    con = sqlite3.connect(path_db)
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO queue (user, filename, text, flag) VALUES (?, ?, ?, ?)",(user, filename, text, ''))
    except sqlite3.Error as e:
    	print(e)
    con.commit()
    con.close()

# 変換待ちのテキストキューから一つ取得する
def get_textqueue():

    con = sqlite3.connect(path_db)
    cur = con.cursor()
    try:
        cur.execute("SELECT user, filename, text FROM queue where flag <> 'done' ")
    except sqlite3.Error as e:
        print(e)
    list = cur.fetchone()
    con.close()
    return list

# 変換待ちの一覧を取得する
def get_textqueue_lists():

    con = sqlite3.connect(path_db)
    cur = con.cursor()
    try:
        cur.execute("SELECT user, filename, text FROM queue where flag <> 'done' ")
    except sqlite3.Error as e:
        print(e)
    lists = cur.fetchall()
    con.close()
    return lists


# 変換済みフラグをセットする
def set_done_textqueue(filename):

    # execute sql
    con = sqlite3.connect(path_db)
    cur = con.cursor()
    try:
        cur.execute("UPDATE queue SET flag = 'done' where filename = ?" ,(filename, ))
    except sqlite3.Error as e:
    	print(e)
    con.commit()
    con.close()


