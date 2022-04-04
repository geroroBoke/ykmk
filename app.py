# from flask import Flask, render_template, request, make_response, redirect
import flask
import gtt
import log
app = flask.Flask(__name__)
app.secret_key = 'super secret string'

# load blueprint
app.register_blueprint(gtt.gtt_bp)
app.register_blueprint(log.log_bp)

# init login manager
log.init_login_manager(app)

# top page
@app.route('/')
def index():
    html = flask.render_template('index.html')
    return html

# list page
@app.route('/list')
def list():
    return gtt.get_mp3info_html()
# #
# @app.route('/', methods=['POST'])
# def check():
#     # get parameters from request
#     text = request.form['text']
#     lower = request.form.get('lower')
#     hidetext = request.form.get('hidetext')

#     if lower:
#         text = text.lower()

#     #do Wordlevelcheck
#     scouter = WordLevelScouter(text)
#     # scouter.retrieveResultMylevel()

#     # stash lastdata
#     global lastdata
#     lastdata["scouter"] = scouter
#     lastdata["text"] = text
#     lastdata["hidetext"] = hidetext

#     #render html
#     html = render_template('index.html', \
#         text=text, newtext = scouter.newtext,\
#         table = scouter.table, \
#         hidetext = hidetext,
#         # ukus = ukus,
#         lower = lower)

#     return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
