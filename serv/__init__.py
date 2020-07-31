from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from serv.encryptDecrypt import load_key
import pathlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd8f9c93ac18d163fcba715854fea0b41'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = str(pathlib.Path(__file__).parent.absolute()) + '\\static\\uploads\\'
app.config['EXPIRATION_TIME_DAYS'] = 30
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024  # 2GB upload limit
db = SQLAlchemy(app)
key = load_key()

from serv import routes
from serv import fileCleanup


# fileCleanup.runFileCleanup()
