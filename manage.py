from core import app
from core import db
from core.manager import MinitManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.engine.url import make_url
from sqlalchemy_utils import database_exists, create_database

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('minit', MinitManager)

url = make_url(app.config['SQLALCHEMY_DATABASE_URI'])
if not database_exists(url):
    create_database(url, encoding='utf8mb4')


from modules.models import Model1 

if __name__ == '__main__':
    manager.run()