from flask import Flask, render_template
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

def create_app():
    app=Flask(__name__)
    app.debug=True
    app.secret_key='thisisasecretkey122'

    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///storage.db'

    db.init_app(app)

    bootstrap = Bootstrap4(app)

    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from .views import mainbp
    app.register_blueprint(mainbp)

    from .auth import bp
    app.register_blueprint(bp)

    from . import events
    app.register_blueprint(events.bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template('error.html'),404


    return app