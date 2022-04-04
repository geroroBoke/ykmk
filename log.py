import flask
import flask_login


# Blueprintオブジェクトを生成
log_bp = flask.Blueprint('log', __name__)

# users data
users = {'geroropad@gmail.com': {'password': 'password'}}

login_manager = flask_login.LoginManager()

# init login manager
def init_login_manager(app):
    login_manager.init_app(app)

class User(flask_login.UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return flask.redirect('/login')

@log_bp.route('/logout', methods=['GET'])
def logout():
    flask_login.logout_user()
    return flask.redirect('/')

@log_bp.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''
    email = flask.request.form['email']
    if email in users:
        if flask.request.form['password'] == users[email]['password']:
            user = User(email)
            flask_login.login_user(user)
            return flask.redirect('/')

    return 'Bad login'
