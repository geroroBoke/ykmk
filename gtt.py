import flask
from gtts import gTTS
from flask_login import current_user
import urllib.parse
import os
import hashlib
from textinfo import get_text_info
from id3 import set_id3_tag
import db

dir_mp3 = r'mysite/mp3/'

# Blueprintオブジェクトを生成
gtt_bp = flask.Blueprint('gtt', __name__)

@gtt_bp.route('/gtts', methods=['POST'])
def gtts_post():

    # get text from form
    text = flask.request.form['text']
    lang = "ja"

    # get text info
    info = get_text_info(text)

    # get filename
    if info:
        filename = "『{0}』({1}){2}-{3}".format(
            info['title'],
            info['number'],
            "", # info['chapter'],
            info['episode'])
        filename = filename.replace('/', '-')
        filename = filename + ".mp3"
    else:
        filename = text.splitlines()[0]
        filename = filename[0:30] + ".mp3"

    # get content
    if info:
        content = info['chapter'] + ", "+ info['episode'] + ", " + info['content']
    else:
        content = text

    # replace
    content = content.replace('\n', '')
    content = content.replace('\r', '')

    # get sound from server
    tts =gTTS(text=content, lang=lang)

    # save file
    try:
        tts.save(dir_mp3 + filename)
    except Exception as e:
        print(e)
        return "failed"

    # id3 tag edit
    if info:
        set_id3_tag(
            dir_mp3 + filename,
            title=info['episode'],
            artist=info['author'],
            album=info['title'],
            track_num=info['number'])

    # サイズ取得
    size = os.path.getsize(dir_mp3 + filename)

    # ハッシュ取得
    hashtext = hashlib.md5(content.encode()).hexdigest()

    # ID取得
    try:
        userid = current_user.id
    except:
        userid = "guest"

    # register in db
    db.put_mp3info(userid, filename, hashtext, size)

    # return mp3 file
    return create_savedfile_response(filename)


# 保存されたファイルをレスポンスにして返す
def create_savedfile_response(filename):

    # get data
    try:
        with open(dir_mp3 + filename, 'rb') as f:
            data = f.read()
    except Exception as e:
        print(e)
        return "file not found"

    # get url-encoded-filename
    url_filename = urllib.parse.quote(filename)

    # return response
    res = flask.make_response(data)
    res.headers['Content-Type'] = 'audio/mpeg'
    res.headers['Content-Disposition'] = "attachment;  filename='{}'; filename*=UTF-8''{}".format(url_filename, url_filename)
    return res


# 指定されたファイルを返す
@gtt_bp.route('/download', methods=['GET'])
def download():

    # get data
    filename = flask.request.args.get("filename")

    # return mp3 file
    return create_savedfile_response(filename)

# 指定されたファイルを消す
@gtt_bp.route('/delete', methods=['GET'])
def delete():

    # get data
    filename = flask.request.args.get("filename")

    #  databaseにから削除する
    db.del_mp3info(filename)

    # ファイルを削除する
    try:
        os.remove(dir_mp3 + filename)
    except Exception as e:
        print(e)

    # redirect list
    return flask.redirect('/list')


# mp3ファイル情報の一覧をhtmlにして出力する
def get_mp3info_html():

    # html出力用
    html = "<a href='/'>top page</a>"
    html += "<ul>"

    # dbからファイルリストを取得
    list = db.get_mp3info_list()

    # ファイルごとにli項目を作成
    for i, l in enumerate(sorted(list, key = lambda r: r[1])):
        filename = l[1]
        url_filename = urllib.parse.quote(filename)
        html += """
        <li>{0}:{1}
        <a href="download?filename={2}">[download]</a>
        <a href="delete?filename={2}">[delete]</a>
        </li>""".format(i, filename,url_filename)

    # htmlを返す
    html += "</ul>"
    html += "<a href='/'>top page</a>"
    return html

