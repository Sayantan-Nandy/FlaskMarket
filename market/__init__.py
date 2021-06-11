from flask import Flask,render_template
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
app.config['SECRET_KEY'] = '3db71b2131c78a71ec35bbc1'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'                      #Redirects the login_required pages to the login url
login_manager.login_message_category = 'info'
from market import routes