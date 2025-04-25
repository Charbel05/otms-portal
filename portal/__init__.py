from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from dotenv import load_dotenv
import os
load_dotenv()

dbname=os.getenv('DBNAME')
user=os.getenv('USER')
password=os.getenv('PASSWORD')
host=os.getenv('HOST')
port = str(os.getenv('PORT'))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a4548ab07f9b2e1f2acb5d575d36a4e8'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/upload_photos'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
login.login_view = 'login'

from portal import routes