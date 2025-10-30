from flask import Flask
from flask_login import LoginManager
from app.Models import db, User
from app.chat.chat_routes import chat_bp
from app.user.user_routes import user_bp
# from ChatR.chat_routes import chat_bp
def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:muhammad%40555@localhost/chat'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dh3qjr3j432k43k4n3kjj4jj44j'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user_bp.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))




    
    app.register_blueprint(chat_bp)
    app.register_blueprint(user_bp)

    return app
