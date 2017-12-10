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

from modules.models import * 

@manager.command
def filldb():
    user1 = User(username="coyote",password="coyote",role=roles["customer"])
    user2 = User(username="baymax",password="baymax",role=roles["sales"])
    user3 = User(username="kevin",password="kevin",role=roles["engineering"])
    user4 = User(username="emmet",password="emmet",role=roles["production"])
    user5 = User(username="panda",password="panda",role=roles["finance"])
    user6 = User(username="ralph",password="ralph",role=roles["test"])

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.add(user6)

    product1 = Product(name = "ACME EARTHQUAKE PILLS", picture = "acme_earthquake.jpg", description="ACME Earthquake Pills are guaranteed to create huge tremors anywhere,\n"+
            "except when used on road runners, of course")
    product2 = Product(name = "ACME GLUE", picture = "acme_glue.jpg", description=" ACME Glue is guaranteed to adhere to anything, just be sure not to cover yourself in it while holding a lit stick of dynamite")
    product3 = Product(name = "ACME GIANT KITE KIT", picture = "acme_kite.jpg", description=" With the ACME Giant Kite Kit and you'll be in the air in no time. However, carrying bombs while using the kite is NOT advisable")
    product4 = Product(name = "ACME BAT-MAN'S OUTFIT", picture = "acme_batman.jpg", description=" Available in several sizes, including regular, the ACME Bat-Man's Outfit will have you flying like a bat in no time")
    product5 = Product(name = "ACME BOOK OF MAGIC", picture = "acme_magic.jpg", description="ACME book of magic")

    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)
    db.session.add(product4)
    db.session.add(product5)

    db.session.commit()
    print("inserting database data done.")
    import shutil,os,glob
    for filename in glob.glob(os.path.join("sample-data", '*.*')):
        shutil.copy(filename, "core/static/img/")
    print("copying images done.")
    

if __name__ == '__main__':
    manager.run()

