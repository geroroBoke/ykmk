import flask
# import threading
import urllib.parse
import os
import hashlib
from gtts import gTTS
from flask_login import current_user
from textinfo import get_text_info
from id3 import set_id3_tag
import db
from mp3 import dir_mp3

# Blueprintオブジェクトを生成
gtt_bp = flask.Blueprint('gtt', __name__)

@gtt_bp.route('/enqueue', methods=['POST'])
def enqueue():

    # get text from form
    text = flask.request.form['text']

    # get filename
    filename = get_filename(text)

    # ID取得
    try:
        userid = current_user.id
    except:
        userid = "guest"

    # dbにenqueueする
    db.put_textqueue(userid, filename, text)

    # return message
    html = "request accpeted :" + small_tag(filename)
    html += "<br><br>"
    html += get_textqueue_html()
    return html
    # return mp3 file
    # create_savedfile_response(filename)

# dequeue
@gtt_bp.route('/dequeue')
def dequeue():

    # queueから一つ取得
    list = db.get_textqueue()

    if not list:
        return "No queue for gtts"

    # listの中身を取得
    userid = list[0]
    filename = list[1]
    text = list[2]

    # gttsしてdbに登録する
    result = gtts_saving_procedure(userid, text)

     # エラーで無ければdoneフラグを立てる
    if not "!error!" in result:
        db.set_done_textqueue(filename)

    # html = result + small_tag(filename)
    # html += "<br><br>"
    # if not "!error!" in result:
    #     html += "<a href='/dequeue'>gtts from queue<span id='tm_left'></span></a>"
    return result

# dequeue
@gtt_bp.route('/process')
def process():

    # queueから一つ取得
    list = db.get_textqueue()

    if not list:
        return "No queue for gtts"

    # listの中身を取得
    filename = list[1]

    html = flask.render_template('process.html', filename=filename)
    return html

@gtt_bp.route('/gtts', methods=['POST'])
def gtts():

    # get text from form
    text = flask.request.form['text']

    # get filename
    filename = get_filename(text)

    # ID取得
    try:
        userid = current_user.id
    except:
        userid = "guest"

    # gttsしてdbに登録する
    result = gtts_saving_procedure(userid, text)

    html = ""
    html += result + "<br>"
    html += small_tag(filename) + "<a href='/mp3/{0}'>Play</a>".format(filename) + "<br>"
    html += "<a href='/'>top page</a>"
    return html

# textからfilename取得
def get_filename(text):

    # text分析をかける
    info = get_text_info(text)
    if info:
        # numberを書き換える "1/100" >> "001/100"
        pos = info['number'].find("/")
        if pos:
            numerator = info['number'][:pos].strip()
            denominator = info['number'][pos+1:].strip()
            # format_text = "{0:0=" + str(len(denominator)) + "}"
            numerator = format(int(numerator), "0=" + str(len(denominator)))
            info['number'] = numerator + "/" + denominator

        # filenameの作成
        filename = "『{0}』({1}){2}-{3}".format(
            info['title'],
            info['number'],
            "", # info['chapter'],
            info['episode'])
        filename = filename.replace('/', '-')
        return filename + ".mp3"
    else:
        return text.splitlines()[0][0:30] + ".mp3"

# gTTSして保存してDBに登録する
def gtts_saving_procedure(userid, text):

    # get text info
    info = get_text_info(text)

    # get_filename
    filename = get_filename(text)

    #
    print("gtts_saving_procedure:" + filename)

    # get content
    if info:
        content = ""
        content += info['episode'] + ", "
        content += info['chapter'] + ", "
        # content += info['title'] + ", "
        content += "。"
        content += info['content'] + ". "
        # content = info['chapter'] + ", "+ info['episode'] + ", " + info['content']
    else:
        content = text

    # エラー回避のおまじない
    content = content.replace('\n', ',')
    content = content.replace('\r', ',')
    content = content.replace('　', '') # 全角スペース

    # ハッシュ取得
    hash = hashlib.md5(content.encode()).hexdigest()

    # 同一ハッシュがあればreturnする
    if db.check_mp3info_exist(hash):
        return "same content file already exists:"

    # get sound from server
    tts =gTTS(text=content, lang="ja")

    # save file
    try:
        tts.save(dir_mp3 + filename)
    except Exception as e:
        print(e)
        return "!error! gtts file saving failed:"

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

    # register in db
    db.put_mp3info(userid, filename, hash, size)

    return "successfully generated mp3:"


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

# list page
@gtt_bp.route('/list')
def list():
    html = """
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=yes" />
    </head>
    <script src="/static/jquery-3.5.0.min.js"></script>
    <script>
    $(function() {
        $('.confirm').click(function(e) {
            e.preventDefault();
            if (window.confirm("Are you sure?")) {
                location.href = this.href;
            }
        });
    });
    </script>
    """
    html += "<a href='/'>top page</a>"
    html += get_mp3info_html()
    html += "<a href='/'>top page</a>"
    return html

# wait_list page
@gtt_bp.route('/w_list')
def w_list():
    html = ""
    html += get_textqueue_html()
    return html

# mp3待ちリストを取得する
def get_textqueue_html():

    # dbからファイルリストを取得
    lists = db.get_textqueue_lists()

    # html作成
    html = ""
    html += "<ol>"
    # for i, l in enumerate(sorted(lists, key = lambda r: r[1])):
    # for i, l in enumerate(lists):
    for l in lists:
        filename = l[1]
        html += "<li>{0}</li>\r\n".format(filename)
    html += "</ol>"

    return html

# small tagをつける
def small_tag(text):
    return "<span style='font-size: x-small'><i>{0}</i></span>".format(text)


# mp3ファイル情報の一覧をhtmlにして出力する
def get_mp3info_html():

    # dbからファイルリストを取得
    lists = db.get_mp3info_lists()

    # htmlを作成する
    html = "<ol>"
    # for i, l in enumerate(sorted(lists, key = lambda r: r[1])):
    for l in sorted(lists, key = lambda r: r[1]):

        # ファイルごとにli項目を作成
        filename = l[1]
        url_filename = urllib.parse.quote(filename)
        # <audio src="{1}" preload="metadata" controls></audio>
        html += """
        <li>
        <span style="font-size:smaller">
        {0}
        <a href="/mp3/{1}">[Play]</a>
        <a href="download?filename={1}">[Download]</a>
        <a href="delete?filename={1}" class="confirm" >[Delete]</a>
        </span><br>
        </li>""".format(filename,url_filename)
    html += "</ol>"
    return html

