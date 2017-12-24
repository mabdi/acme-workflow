import core.config
import logging
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler
from datetime import datetime,timedelta

# flask object
app = Flask(__name__, static_path="/static")

# configs
app.config.update(
    SESSION_COOKIE_PATH=core.config.session_cookie_path,
    SESSION_COOKIE_NAME=core.config.session_cookie_name, 
    SECRET_KEY=core.config.secret_key,
    SQLALCHEMY_DATABASE_URI=core.config.sqlalchemy_database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)
app.permanent_session_lifetime = timedelta(minutes=20)



# db
db = SQLAlchemy(app)

# logging
logger = app.logger
handler = RotatingFileHandler('server.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# blueprints
from modules.routes import bp_order
from modules.routes import bp_captcha

app.register_blueprint(bp_order.blueprint, url_prefix= core.config.url_prefix + "/order")
app.register_blueprint(bp_captcha.blueprint, url_prefix= core.config.url_prefix + "/captcha")