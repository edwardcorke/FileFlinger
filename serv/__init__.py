from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, pathlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd8f9c93ac18d163fcba715854fea0b41'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = str(pathlib.Path(__file__).parent.absolute()) + '\\static\\uploads\\'
db = SQLAlchemy(app)

from serv import routes
from serv import fileCleanup


fileCleanup.runFileCleanup()
