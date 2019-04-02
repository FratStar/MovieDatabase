from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#import flask.ext.whooshalchemy as wa

#establishes connection to database and sets up a backend Flask application to serve as a means to connect to the DB

dbuser = 'SA'
dbpass = 'CIS-PASS2019'
dsn = 'localdsn'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://{dbuser}:{dbpass}@{dsn}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
#app.config['WHOOSH_BASE'] = 'whoosh'
db = SQLAlchemy(app)
