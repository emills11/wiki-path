from flask import Flask
from flask import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config.from_object(Config)

from app import routes

bootstrap = Bootstrap(app)