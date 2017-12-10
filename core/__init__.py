import core.config
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler

# flask object
app = Flask(__name__, static_path="/static")

# configs
app.config["SESSION_COOKIE_PATH"] = core.config.session_cookie_path
app.config["SESSION_COOKIE_NAME"] = core.config.session_cookie_name
app.secret_key = core.config.secret_key
app.config['SQLALCHEMY_DATABASE_URI']  = core.config.sqlalchemy_database_uri
app.config['APPLICATION_ROOT'] = '/aos4dev'



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

app.register_blueprint(bp_order.blueprint, url_prefix="/order")
app.register_blueprint(bp_captcha.blueprint, url_prefix="/captcha")