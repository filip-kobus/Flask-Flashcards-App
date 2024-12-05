from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flashcardmaker.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail(app)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flashcardmaker.users.routes import users
    from flashcardmaker.main.routes import main
    from flashcardmaker.flashcards.routes import flashcards
    from flashcardmaker.directories.routes import directories

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(flashcards)
    app.register_blueprint(directories)

    return app

