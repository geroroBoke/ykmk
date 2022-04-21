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

@app.route("/mp3/<path:filename>")
def play(filename):
    return flask.send_from_directory("mp3", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, ) #threaded=True)
