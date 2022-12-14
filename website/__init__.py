from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'BryanAndCalebProject'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME
    db.init_app(app)

    from .auth import auth
    from .views import views
    from .administrator import administrator

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(administrator, url_prefix='/admin')

    from .models import User
    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

def create_db(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Database created.', flush=True)