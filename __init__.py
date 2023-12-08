from flask import Flask
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pgsdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'coolaf'
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)
