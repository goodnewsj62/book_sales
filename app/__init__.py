from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from configuration import Config



db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()

def create_app(config=Config()):
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_object(config)

    #init dependencies
    db.init_app(app)
    login_manager.init_app(app=app)
    migrate.init_app(app=app)
    mail.init_app(app=app)

    with app.app_context():
        #all your blueprint registration 
        pass
    return app
